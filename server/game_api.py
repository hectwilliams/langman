from flask import g
from flask_restx import  Resource, Api, Namespace
from sqlalchemy.sql import func 
from .langman_orm import Usage, User, Game
import flask_jwt_extended as JWT 

import datetime
import uuid
from unidecode import unidecode 

games_api = Namespace('games', description='Creating and playing games')

# /games ( /api/games )
@games_api.route('')
class Games(Resource):
    valid_langs = ['en', 'es', 'fr']

    @JWT.jwt_required()
    def post(self):
        '''
            Start a new game and return web token housing game id

            :route: ``/`` POST 

            :payload:
                * ``username`` A string containing the player's name
                * ``language`` Language to play in (e.g. 'en')

            :returns:
                A successful message:
                    * ``message`` Literal `success`
                    * ``game_id`` The new game's UUID
                    * ``access_token`` Web Token
        '''

        if not (games_api.payload and 'language' in games_api.payload) :
            games_api.abort(400, 'New game POST requires language')
        
        lang = games_api.payload['language']
        
        # user's name from token
        name = JWT.get_jwt()['name']  
        # user's id from token 
        user_id = JWT.get_jwt_identity()

        if len(name.strip()) == 0 or lang not in self.valid_langs:
            games_api.abort(400, 'invalid username or language not supported') # bad request

        # create/get user record (if it exists) **
        user = g.games_db.query(User).filter(User.user_id == user_id).one_or_none() 

        # no user record found 
        if user == None:
            user = User(user_id = user_id, user_name= name, first_time=datetime.datetime.now())
            # add user to User table 
            g.games_db.add(user)
            g.games_db.commit() 
            user = g.games_db.query(User).filter(User.user_name == name).one()

        # update user fields (game has started)
        user._game_started(lang)

        # select a usage example ( i.e. game set)
        usage = g.usage_db.query(Usage).filter(Usage.language == lang).order_by(func.random()).first()

        # create the new game **
        new_game_id = str(uuid.uuid4()) # random game id  - uuid4 creates a new id
        new_game = Game (game_id = new_game_id, player = user.user_id, usage_id = usage.usage_id, bad_guesses = 0, reveal_word = "_" * len(usage.secret_word), start_time = datetime.datetime.now())

        # add game to Game table 
        g.games_db.add(new_game)
        g.games_db.commit()
        
        access_token = JWT.create_access_token(identity=user_id, additional_claims={'access':'player' , 'name':name, 'game_id': new_game_id })
        
        return {'message': 'success', 'game_id': new_game_id, 'access_token': access_token}


# /games/1 ( /api/games/1 )
@games_api.route('/<game_id>')
class OneGame(Resource):
    
    @JWT.jwt_required()
    def get(self, game_id):
        '''
            Get the state/information of the game. General token in ( to server) , game-specific token out ( to client or service )

            :route: ``/`` GET

            :returns: 
                The object's properties per game:
                    * ``game_id`` The game UUID 
                    * ``player`` The player's name
                    * ``usage_id`` The game usage id from Usages table 
                    * ``guessed`` A string of guessed letters 
                    * ``reveal_word`` Guessed letters in otherwise blanked word strings (i.e. blanks and revealed letters so far)
                    * ``bad_guesses`` Number of incorrect guesses so far 
                    * ``start_time`` The epoch ordinal time when game began 
                    * ``end_time`` The epoch ordinal time when game ended
                    * ``result`` Game outcome from ('lost', 'won', 'active') 
                    * ``usage`` The full sentence example with guess-word blanked 
                    * ``lang`` The language of the example, such as 'en'
                    * ``source`` The book from which the usage example originated 
        '''

        # check input(i.e. game_id) is valid 
        game = g.games_db.query(Game).filter(Game.game_id == game_id).one_or_none()

        # ensure valid game using web token 
            # game exist
            # current player matches token's player 
            # game_id should not exist within general token 
        if (game is None or game.player != JWT.get_jwt_identity() or 'game_id' in JWT.get_jwt()):
            games_api.abort(404, 'Game{} is unauthorized or nonexistent'.format(game_id))
        
        # get usage record 
        usage = g.usage_db.query(Usage).filter(Usage.usage_id == game.usage_id).one()

        #return game state
        game_dict = game._to_dict() 
        game_dict['usage'] = usage.usage.format( word = '_' * len(usage.secret_word) )  # " hi {word}".format(word='*' * 3)" = "hi ***""
        game_dict['lang'] = usage.language
        game_dict['source'] = usage.source 
        
            # new token with game_id claim 
        game_dict['access_token'] = JWT.create_access_token(identity=JWT.get_jwt_identity(), additional_claims={'access': 'player' , 'game_id': game_id, 'name': JWT.get_jwt()['name'] })
        return game_dict 
    
    @JWT.jwt_required()
    def put(self, game_id):
        '''
            Modify state/record.
            
            Guess letter and update the game state accordingly 

            :route: ``/<game_id>`` PUT

            :payload: 
                Guessed letter as object type:
                    * ``letter`` A single guessed letter 
            
            :returns:
                The object for a game, including:
                    * ``game_id`` The game's UUID
                    * ``player`` The player name 
                    * ``usage_id`` The game usage id from the Usages table 
                    * ``guessed`` A string of guessed letters 
                    * ``reveal_word``  Guessed letters in otherwise blanked word strings (i.e. blanks and revealed letters so far)
                    * ``bad_guesses`` Number of incorrect guesses so far 
                    * ``start_time`` The epoch ordinal time when game began 
                    * ``end_time`` The epoch ordinal time when game ended 
                    * ``result`` Game outcome from enum ('lost', 'won', 'active')
        '''

        game = g.games_db.query(Game).filter(Game.game_id == game_id).one_or_none()

        if game is None:
            games_api.abort(404, 'Game with id {} does not exist'.format(game_id)) # page/file(i.e. Game) does not exist 
        
        # token includes a valid game_id for a game
        claims = JWT.get_jwt()
        if claims.get('game_id', '') != game_id:
            games_api.abort(503, 'Unauthorized access to game {}'.format(game_id))


        if game._result() != 'active':
            games_api.abort(403, 'Game with id {} is over'.format(game_id) ) # requesting on nonactive game, session is forbidden 
        
        old_dict = game._to_dict()  # current game record

        if ('letter' not in games_api.payload or not games_api.payload['letter'].isalpha() or len(games_api.payload['letter']) != 1 ):
            games_api.abort(400, 'PUT requires one alphabetic character in letter field') # bad request 
         
        letter = games_api.payload['letter'].lower() 

        if letter in game.guessed: 
            games_api.abort(403, 'Letter {} was already guessed'.format(letter))
        
        game.guessed = game.guessed + letter 

        usage = g.usage_db.query(Usage).filter(Usage.usage_id == game.usage_id).one() 

        # update reveal_word if a correct guess is found  + handle diacritics 
        if letter in unidecode(usage.secret_word.lower()):
            game.reveal_word = ''.join([ l if unidecode(l.lower()) in game.guessed else '_' for l in usage.secret_word  ]) # Note: unidecode(å) = a  
        else:
            game.bad_guesses += 1

        # handle if game is over, update user record 
        outcome = game._result()
        if outcome != 'active':
            user = g.games_db.query(User).filter(User.user_id == game.player).one() 
            game.end_time = datetime.datetime.now()
            user._game_ended(outcome, game.end_time - game.start_time)
        
        # return game state 
        game_dict = game._to_dict(old_dict) # consistency check (TBD)
        if game_dict == None:
            games_api.abort(409, "request malforms resource")
        
        game_dict['usage'] = usage.usage.format(word='_'*len(usage.secret_word))    
        game_dict['lang'] = usage.language 
        game_dict['source'] = usage.source

        # win or loss store secret word 
        if outcome != 'active':
            game_dict['secret_word'] = usage.secret_word
        
        g.games_db.commit()
        
        return game_dict
    
    @JWT.jwt_required()
    def delete(self, game_id):
        '''
            Delete record for game ``game_id``

            :route: ``/<game_id>`` DELETE 

            :returns:
                An acknowledgment object:
                    * ``message`` Either `One` or `Zero` records deleted 
            
            This method removed the game from its table 
        '''
        # token includes a valid game_id for a game(i.e. token housing game_id matches the current active game (i.e. game_id))
        claims = JWT.get_jwt_claims()
        if claims.get('game_id', '') != game_id:
            games_api.abort(503, 'Unauthorized access to game {}'.format(game_id) )

        game = g.games_db.query(Game).filter(Game.game_id == game_id).one_or_none() 

        if game is not None:
            g.games_db.delete(game)
            g.games_db.commit()
            msg = 'One record delete'
        else:
            msg = 'No record deleted'
        
        return {'message': msg}
    

