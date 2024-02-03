import uuid 

from flask import g 
from flask_restx import Resource, Namespace, Api
import flask_jwt_extended as JWT 
import sqlalchemy
from sqlalchemy.orm import exc
from .auth_orm import Auth 
import datetime

auth_api = Namespace('auth', description='Authentication')

@auth_api.route('')
class Authenticate(Resource):
    def post(self):
        '''
            Register a new user and log them in 

            :route: ``/`` GET
            :payload:
                User's credentials
                    * ``username`` Player's name (a string)
                    * ``passsword`` Password (a string)
            :returns:
                The token within a JSON object:
                    * ``access_token`` The JSON web token for this session
        '''

        # 1. make sure you have all the arguments you need 
        if not (auth_api.payload and 'username' in auth_api.payload and 'password' in auth_api.payload): 
            auth_api.abort(400, 'username and password required')

        # 2 create record for account 
        user_id = str(uuid.uuid3(uuid.NAMESPACE_URL, auth_api.payload['username']))
        user_auth = Auth  ( user_name = auth_api.payload['username'] , user_id = user_id, pass_salt=uuid.uuid1().hex )
        user_auth._set_hash(auth_api.payload['password'])
        g.auth_db.add(user_auth)

        try:
            g.auth_db.commit()
        except exc.sa_exc.IntegrityError:
            auth_api.abort(400, 'Username is already registered')
        
        # 3 create and return the access toek for the user  expires_delta=datetime.timedelta(minutes=60)
        access_token = JWT.create_access_token(identity=user_id,additional_claims={'access': 'player', 'name': auth_api.payload['username'] })
        return {'access_token': access_token }
        
    def put (self):
        '''
            Login into existing account

            :route: ``/`` PUT 
            :payload: 
                User's credentials
                    * ``username`` Player's name (a string)
                    * ``password`` Password (a string)
            :returns:
                The token within a JSON object:
                    * ``access_token`` The JSON web token for this session
        '''

    # 1. make sure you have all the arguments you need 
        if not (auth_api.payload and 'username' in auth_api.payload and 'password' in auth_api.payload): 
            auth_api.abort(400, 'username and password required')
    
    # 2. check that the password is valid ( to be filled in later)
        user_auth = g.auth_db.query(Auth).filter(Auth.user_name == auth_api.payload['username']).one_or_none() 
        if user_auth is None or (not user_auth._check_password(auth_api.payload['password'])  ):
            return {'message': 'Invalid credentials'}, 401
    
    # 3 create and return the access token for the user if valid 
        access_token = JWT.create_access_token(identity=user_auth.user_id, additional_claims={'access': 'player', 'name': user_auth.user_name })
        return {'access_token': access_token}

    @JWT.jwt_required()
    def get(self):
        '''
            Test the access token, passed in as authorization header

            :route: ``/`` GET

            :returns:
                The token within a JSON object:
                    * ``logged_in_as`` The user's name (string)
                    * ``additional_claims`` The user's access claims (dict)
        '''
        return {'logged_in_as': JWT.get_jwt_identity(),  'additional_claims': JWT.get_jwt() }

    @JWT.jwt_required()
    def delete(self):
        '''
            Remove the user record

            :route: ``/`` DELETE

            :returns:
                The token within a JSON object:
                    * ``deleted_user_id`` The user id (string)
        '''
        user_id = JWT.get_jwt_identity() 
        user_auth = g.auth_db.query(Auth).filter(Auth.user_id == user_id).one_or_none() 
        if user_auth is not None:
            g.auth_db.delete(user_auth)
            g.auth_db.commit() 

        return {'deleted_user_id': user_id }