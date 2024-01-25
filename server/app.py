import os
from flask import Flask , g
from flask_restx import  Resource, Api, Namespace
from flask_cors import CORS 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func 

from .util import get_config 
from .langman_orm import Usage, User, Game

import datetime
import random 
import uuid

# namespace 
games_api = Namespace('games', description='Creating and playing games')

# create/configure app 
app = Flask(__name__)
config = get_config( os.environ['FLASK_ENV'], open('server/config.yaml'))
app.config.update( config ) 

CORS(app) # cross origin resource sharing 

# create Restplus api on app
api = Api(app) 
api.add_namespace(games_api, path='/api/games') # insert games namespace , client expects /games; changed to /api/games 


@app.before_request
def init_db():
    '''
        Initialize db by creating the global db_session
        
        runs on each request; global flask variable g is a global session
    '''

    if not hasattr(g, 'usage_db'):
        db_usage = create_engine(config['DB_USAGE'])
        g.usage_db = sessionmaker(db_usage)()

    if not hasattr(g, 'games_db'):
        db_games = create_engine(config['DB_GAMES'])
        g.games_db = sessionmaker(db_games)()

@app.teardown_request
def close_db(exception):
    '''
        close down db connection; same one cannot be used 

        clobe db after request is complete 
    '''
    
    if hasattr(g, 'usage_db'):
        g.usage_db.close()
        _ = g.pop('usage_db')

    if hasattr(g, 'games_db'):
        g.games_db.close()
        _ = g.pop('games_db')


# /games ( /api/games )
@games_api.route('')
class Games(Resource):
    valid_langs = ('en', 'es', 'fr')
    def post(self):
        '''
            Start a new game and return the game id

            :route: ``/`` GET 

            :payload:
                * ``username`` A string containing the player's name
                * ``language`` Language to play in (e.g. 'en')

            :returns:
                A successful message:
                    * ``message`` Literal `success`
                    * ``game_id`` The new game's UUID
        '''
        # validate input (i.e payload)
        if not (games_api.payload and 'username' in games_api.payload and 'language' in games_api.payload):
            games_api.abort(400, 'new Game POST requires username and language ') # bad request

        lang = games_api.payload['language']
        name = games_api.payload['username']
        user_id = str(uuid.uuid3(uuid.NAMESPACE_URL, name)) #uuid3 hashes a string in deterministically

        # handle incorrect selected language 
        if lang not in self.valid_langs:
            return {'message': 'New game POST language must be from ' + ', '.join(Games.valid_langs) }
        
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
        return {'message': 'success', 'game_id': new_game_id}
    
# /games/1 ( /api/games/1 )
@games_api.route('/<game_id>')
class OneGame(Resource):
    def get(self, game_id):
        '''
            Get the state/information of the game

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

        # error handle if no game_id exist 
        if game is None:
            games_api.abort(404, 'Game with id {} does not exist'.format(game_id)) # requested page/file does exist 
        
        # get usage record 
        usage = g.usage_db.query(Usage).filter(Usage.usage_id == game.usage_id).one()

        #return game state
        game_dict = game._to_dict() 
        game_dict['usage'] = usage.usage.format( word = '_' * len(usage.secret_word) )  # " hi {word}".format(word='*' * 3)" = "hi ***""
        game_dict['lang'] = usage.language
        game_dict['source'] = usage.source 

        return game_dict 
    
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

        # error handle user input/requests 
        if game is None:
            games_api.abort(404, 'Game with id {} does not exist'.format(game_id)) # page/file does not exist 
        
        if game._result() != 'active':
            games_api.abort(403, 'Game with id {} is over'.format(game_id) ) # requesting on nonactive game, session is forbidden 
        
        if ('letter' not in games_api.payload or not games_api.payload['letter'].isalpha() or len(games_api.payload['letter']) != 1 ):
            games_api.abort(400, 'PUT requires one alphabetic character in letter field') # bad request 
         
        letter = games_api.payload['letter'].lower() 

        if letter in game.guessed: 
            games_api.abort(403, 'Letter {} was already guessed'.format(letter))
        
        game.guessed = game.guessed + letter 

        usage = g.usage_db.query(Usage).filter(Usage.usage_id == game.usage_id).one() 

        # update reveal_word if a correct guess is found 
        if letter in usage.secret_word.lower():
            game.reveal_word = ''.join(l if l.lower() in game.guessed else '_' for l in usage.secret_word) #  reveal_word is updated upon a matched guess 
        else:
            game.bad_guesses += 1

        # handle gameover, update user record 
        outcome = game._result()
        if outcome != 'active':
            user = g.games_db.query(User).filter(User.user_id == game.player).one() 
            game.end_time = datetime.datetime.now()
            user.__game_ended(outcome, game.end_time - game.start_time)
        
        # return game state 
        game_dict = game._to_dict() 
        game_dict['usage'] = usage.usage.format(word='_'*len(usage.secret_word))    
        game_dict['lang'] = usage.language 
        game_dict['source'] = usage.source
        if outcome != 'active':
            game_dict['secret_word'] = usage.secret_word
        
        g.games_db.commit()
        
        return game_dict

    def delete(self, game_id):
        '''
            End the game, delete the state/record
        '''
        return {'message': 'Game DELETE Under Construction'}
    

