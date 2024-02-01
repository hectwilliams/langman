import os
import csv
import click 
from .langman_orm import  Usage, Game, User
from .util import get_config
from flask import Flask 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
import json 
import datetime

# Note: export the following:
## FLASK_APP : server.prepare_orm.py
## FLASK_ENV : dev_lite{ for lite } dev_postgres{ for postgres }

'''
    # Note: export the following:
    ## FLASK_APP : server.prepare_orm.py
    ## FLASK_ENV : dev_lite{ for lite } dev_postgres{ for postgres }

    In langman directory run the following command:
        flask init-db 
'''

# flask instance 
app = Flask(__name__)

# register the client command init-db 
@app.cli.command('init-db')
def init_db():
    config = get_config( os.environ['FLASK_ENV'], open('server/config.yaml'))
    init_db_task(config)

def init_db_task(config):

    # create games database
    db = create_engine(config['DB_GAMES'])
    inspector = inspect(db)
    #drop table if table(s) exist(s)
    if inspector.get_table_names():
        Game.__table__.drop(db)
        User.__table__.drop(db)
    # #create table(s)
    Game.__table__.create(db)
    User.__table__.create(db)

    # Base.metadata.create_all(db)  # base creates tables using all derived classes in langman_orm.py

    # create usages database 
    db = create_engine(config['DB_USAGE'])
    #drop table if table(s) exist(s)
    if inspector.get_table_names():
        Usage.__table__.drop(db)
    # #create table(s)
    Usage.__table__.create(db)
    
    # create session for usages database
    session = (sessionmaker(db))()
    
    # copy .csv data into database 
    csv_path = os.path.join(os.path.dirname(__file__) , "../", 'data', 'usages.csv')
    if session.query(Usage).count() == 0:
        with open(csv_path) as f:
            # modify record to meet usage object type requirement
            read_collection = list(csv.reader(f))
            for index, record in enumerate(read_collection):
                read_collection[index] = Usage(
                    usage_id = int(record[0]),
                    language =  record[1] ,
                    lang_id =  int(record[2]) ,
                    secret_word = record[3],
                    usage = record[4],
                    source = record[5]
                )
            # write to table 
            session.add_all(read_collection)
            session.commit()