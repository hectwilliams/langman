from sqlalchemy import  Column, types 
from sqlalchemy.orm import DeclarativeBase
import datetime
import json 
from .util import date_to_ordinal

class _Base(DeclarativeBase):
    '''
        Base class 
    '''
    type_annotation_map = {}

class Usage(_Base):
    '''
        Table ``usages`` with fields: 
            * ``usage_id``- UUID primary key string of length 38
            * ``language``- Two-letter language code (en, es, fr)
            * ``lang_id``- language index of the language
            * ``secret_word``- Word to be guesses (length <= 25)
            * ``usage``- Usage sentence, length <= 400, with word blanked 
            * ``source``- Text from which the usage sentence is drawn
    '''

    __tablename__ = 'usages'
    usage_id = Column(types.Integer, primary_key=True)
    language = Column( types.Enum('en','es','fr', name = 'language_codes'), nullable=False)
    lang_id = Column(types.Integer)
    secret_word = Column(types.String(length=25), nullable=False)
    usage = Column(types.String(length=500), nullable=False)
    source = Column(types.String(length=100))

class User(_Base):
    '''
        Table ``users`` with fields:
            * ``user_id`` - UUID primary key of length 38
            * ``user_name`` - String of maximum length 30
            * ``num_games`` - Integer count of games started
            * ``outcomes`` - JSON string storing game counts (win, losses, cancels) by outcome 
            * ``by_lang`` - JSON string storing game counts by game language
            * ``first_time`` - DateTime indicating when first game was played
            * ``total_time`` - TimeDelta of total time with active games
            * ``avg_time`` - TimeDelta of the average game length
    
        Required consistency:
            *   After adding a letter to a game, two outputs are possible
                *   win/lose, changing the num_games property
                *   continued play, no change to num_games property

            *  total languages (User.by_lang) and number of outcomes (User.outcomes) should equal the User.num_games 

            * User.avg_time must always equal User.total_time/User.games 

            * User.guessed is either the same (i.e. start= "ab" end="ab") or  a string with the letter guess appended (i.e. start = ab end = abh)



    '''

    __tablename__ = 'users'
    user_id = Column(types.String(length=38), primary_key=True)
    user_name = Column(types.String(length=40), nullable=False)
    num_games = Column(types.Integer, default = 0)
    outcomes = Column(types.Text, default='{}')
    by_lang = Column(types.Text, default='{}')
    first_time = Column(types.DateTime)
    total_time = Column(types.Interval)
    avg_time = Column(types.Interval)

    def _incr_json_field(self, field, key):
        '''
            Increment the value of self.``field``[``key``] by one where
            field is a JSON text string 
            
            ( Does not commit)
        '''

        d= json.loads(getattr(self, field)) # tranform JSON string to python object 

        d[key] = d.get(key, 0) + 1

        setattr(self, field, json.dumps(d))

    def _decr_json_field(self, field, key):
        '''
            decrement the value of self.``field``[``key``] by one where
            field is a JSON text string 

            ( Does not commit )
        '''

        d= json.loads(getattr(self, field))

        d[key] = d.get(key, 0) - 1

        setattr(self, field, json.dumps(d))

    def _game_started(self, lang):
        '''
            Update the number of games ``num_games`` and both ``outcomes`` and
            ``by_lang`` counts by one.
            
            ( Does not commit)
        '''
        self.num_games = (self.num_games or 0) + 1
        self._incr_json_field('outcomes', 'active')
        self._incr_json_field('by_lang', lang)

    def _game_ended(self, outcome, time_delta):
        '''
            update the ``total_time`` and ``avg_time`` according to a game that took time_delta time. Also, update ``outcomes`` 
            by converting on active game to have outcome ``outcome`` 

            (Does not commit)
        '''

        self._decr_json_field('outcomes', 'active')
        self._incr_json_field('outcomes', outcome)
        self.total_time = time_delta + (self.total_time or datetime.timedelta(0))
        self.avg_time = self.total_time / self.num_games

class Game(_Base):
    '''
        Table ``games`` with fields:
            * ``game_id`` - UUID primary key of length 38
            * ``player`` - Player key from ``users`` table, length 38
            * ``usage_id`` - Integer index usage in ``usages`` table
            * ``guessed`` - A string of the letters guessed so far 
            * ``reveal_word`` - Secret word with guessed letters filled in
            * ``bad_guesses`` - Number of bad guesses so far as an integer
            * ``start_time`` - DateTime when game started
            * ``end_time`` - DateTime when game ended

        Required consistency:
            * player and usage_id never changes 
            * reveal word letters are from guessed string
            * badguess is the count of letters in guessed, not found in reveal_word
    '''

    __tablename__ = 'games'
    game_id = Column(types.String(length=38), primary_key=True)
    player = Column(types.String(length=40), nullable=False)
    usage_id = Column(types.Integer, nullable=False)
    guessed = Column(types.String(length=30), default='')
    reveal_word = Column(types.String(length=25), nullable=False)
    bad_guesses = Column(types.Integer)
    start_time = Column(types.DateTime)
    end_time = Column(types.DateTime)

    def _result(self):
        '''
            Return the result of the game: lost, won, or active 
        '''
        if '_' not in self.reveal_word :
            return 'won'
        elif self.bad_guesses == 6:
            return 'lost'
        else:
            return 'active' 
    
    def _to_dict(self, oldict = None):
        '''
            Convert the game into a dictionary suitable for JSON serialization 
        '''

        as_dict = {k:v for k,v in self.__dict__.items() if not k.startswith('_')}  # dict_items([('exampleKey', 'exampleValue')])
        
        if oldict != None and not self._check_consistent(as_dict, oldict) :
            return None

        as_dict['result'] = self._result() 
        as_dict['start_time'] = date_to_ordinal(as_dict.get('start_time'))
        as_dict['end_time'] = date_to_ordinal(as_dict.get('end_time'))

        return as_dict  
    
    def _check_consistent(self, newdict, olddict):
        output = True

        if (olddict['player'] != newdict['player']   ):
            output = False
            assert False, 'Game.player'
        
        if (olddict['usage_id'] != newdict['usage_id'] ):
            output = False
            assert False, 'Game.usage_id'

        # prev_guess_summary = ''.join( [c if c in olddict['reveal_word']   else  '*'  for c in olddict['guessed']   ] )  #invalid chars in 'guessed' property string are replaced with *
        # curr_guess_summary = ''.join( [c if c in newdict['reveal_word']   else  '*'  for c in newdict['guessed']   ] ) 
        
        # if not (prev_guess_summary== olddict['guessed']   and curr_guess_summary == newdict['guessed']  ) :
        #     output = False 

        # if not (prev_guess_summary.count('*') == olddict['bad_guesses']  and  curr_guess_summary.count('*') == newdict['bad_guesses']):
        #     output = False 
        
        return output 