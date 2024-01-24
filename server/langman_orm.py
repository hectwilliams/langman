from sqlalchemy import create_engine, Column, types, MetaData 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {}

class Usage(Base):
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

class User(Base):
    '''
        Table ``users`` with fields
        * ``user_id`` - UUID primary key of length 38
        * ``user_name`` - String of maximum length 30
        * ``num_games`` - Integer count of games started
        * ``outcomes`` - JSON string storing game counts (win, losses, cancels) by outcome 
        * ``by_lang`` - JSON string storing game counts by game language
        * ``first_time`` - DateTime indicating when first game was played
        * ``total_time`` - TimeDelta of total time with active games
        * ``avg_time`` - TimeDelta of the average game length
    '''

    __tablename__ = 'users'
    user_id = Column(types.String(length=38), primary_key=True)
    user_name = Column(types.String(length=30), nullable=False)
    num_games = Column(types.Integer, default = 0)
    outcomes = Column(types.Text, default='{}')
    by_lang = Column(types.Text, default='{}')
    first_time = Column(types.DateTime)
    total_time = Column(types.Interval)
    avg_time = Column(types.Interval)

class Game(Base):
    '''
        Table ``games`` with fields
        * ``game_id`` - UUID primary key of length 38
        * ``player`` - Player key from ``users`` table, length 38
        * ``usage_id`` - Integer index usage in ``usages`` table
        * ``guessed`` - A string of the letters guessed so far 
        * ``reveal_word`` - Secret word with guessed letters filled in
        * ``bad_guesses`` - Number of bad guesses so far as an integer
        * ``start_time`` - DateTime when game started
        * ``end_time`` - DateTime when game ended
    '''

    __tablename__ = 'games'
    game_id = Column(types.String(length=38), primary_key=True)
    player = Column(types.String(length=30), nullable=False)
    usage_id = Column(types.Integer, nullable=False)
    guessed = Column(types.String(length=30), default='')
    reveal_word = Column(types.String(length=25), nullable=False)
    bad_guesses = Column(types.Integer)
    start_time = Column(types.DateTime)
    end_time = Column(types.DateTime)
