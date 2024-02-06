import os
from flask import Flask , g, Response
from flask_restx import  Resource, Api, Namespace
from flask_cors import CORS 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func 
from .langman_orm import Usage, User, Game
from .util import get_config, init_usage_table
from .prepare_orm import init_db_task
import flask_jwt_extended as JWT 
from .game_api import games_api
from .auth_api import auth_api

# create/configure app 
app = Flask(__name__)
CORS(app) # cross origin resource sharing 

api = Api(app)

api.add_namespace(games_api, path='/api/games')
api.add_namespace(auth_api, path='/api/auth')

jwt = JWT.JWTManager(app)

# handler required for sphinx documentation generation 
try:
    resource = open('server/config.yaml')
    config = get_config( os.environ['FLASK_ENV'] , resource )
    
    if init_usage_table() : # initialize database ? 
        init_db_task(config)
    
    app.config.update( config ) # add flash environ variables and yaml field key values 

except LookupError as error :
    print('error opening yaml file')

@app.before_request
def init_db():
    '''
        Initialize db by creating the global db sessions
        
        runs on each request; global flask variable g is a global session
    '''

    if not hasattr(g, 'usage_db'):
        db_usage = create_engine(app.config['DB_USAGE'])
        g.usage_db = sessionmaker(db_usage)()

    if not hasattr(g, 'games_db'):
        db_games = create_engine(app.config['DB_GAMES'])
        g.games_db = sessionmaker(db_games)()

    if not hasattr(g, 'auth_db'):
        db_auth = create_engine(app.config['DB_AUTH'])
        g.auth_db = sessionmaker(db_auth)()

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

    if hasattr(g, 'auth_db'):
        g.auth_db.close()
        _ = g.pop('auth_db')

