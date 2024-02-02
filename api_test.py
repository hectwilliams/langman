import json, random, os 
import pytest, yaml

from server.app import app 

@pytest.fixture(scope='module')
def test_app():
    '''
        Uses ``app`` imported from flask_app  to create a testable Flask application

        :yield: Flask application with a context, ready for testing
    '''
    # global app 
    app.config['TESTING'] = True 

    #test client 
    test_app = app.test_client() 
    # testc client context (or test sandbox)
    ctx = app.app_context()
    # push context 
    ctx.push() 
    # proces test
    yield test_app 
    # throw away context whe complete 
    ctx.pop() 

def random_string():
    '''
        Create a random string of upper and lower case letters, digits, and punctuation, of length 0, 3, 8, 22 for testing
    '''

    valid_chars =  ('abcdefghijklmnopqrstuvwxyz'
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    '0123456789!@#$%^&*()_-+=~?'
                    )
    return ''.join( 
            [random.choice(valid_chars)     # select random char 
                for i in range(random.choice([0, 3, 8, 22])) ] # random range controls the length of the random string
    )

def test_full_random_game(test_app):
    '''
        Step thru a random game
    '''

    language = random.choice(['en', 'es', 'fr', 'bad'])
    username = random_string() 
    
    # POST to start a game, extract the game_id 
    response = test_app.post('/api/games', data=json.dumps(dict(username=username, language=language)), headers= {'Content-Type': 'application/json', 'Accept': 'application/json' })

    if language == 'bad':
        assert response.status_code == 400, 'Wrong response for language' 
        return # exit current test/game
    
    if len(username) == 0:
        assert response.status_code == 400, 'invalid username'  # TODO LENGTH REQUIREMENT 
        return 

    assert response.status_code == 200, 'Error POSTing for new game'

    game_id = json.loads(response.data.decode())['game_id']

    # GET game state 
    response = test_app.get('/api/games/' + game_id, headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} )

    assert response.status_code == 200, 'Error in Get game'

    game_status = json.loads (response.data.decode())['result']

    # PUT random letters until game is not longer active 
    guesses = '' 
    while game_status == 'active':
        letter = random.choice('abcdefghijklmnopqrstuvwxyz')
        guesses = guesses + letter 
        response = test_app.put('/api/games/' + game_id, data = json.dumps(dict(letter=letter) ), headers = {'Content-Type': 'application/json', 'Accept': 'application/json'  } ) 

        if letter.isalpha():
            # game permits  unique character guesses
            if guesses.count(letter) == 1:
                assert response.status_code == 200, 'Error in PUT letter guess'
                game_status = json.loads(response.data.decode())['result']
            else:
                assert response.status_code == 403, 'Repeated code should be forbidden'
        
        # number of guesses > 100 something is went wrong internally, possible infinite loop 
        assert len(guesses) < 100, 'Too many guesses, something is broken'

    # Game should be over at this point
        
    # CHECK final number of bad_guesses
    game_data = json.loads(response.data.decode())
    
    # two possible  outcomes if game is over 
    if game_data['result'] != 'active':
        loss_assertion  = (game_data['result'] == 'lost') and (game_data['bad_guesses'] == 6 ) 
        win_assertion = (game_data['result'] == 'won') and (game_data['bad_guesses'] < 6 )
        assert   loss_assertion or win_assertion, 'lost game expects a fixed number of bad guesses' + str(game_data['bad_guesses'] ) + ' ' + str(game_data['guessed'] )  + ' ' + guesses

    # TRY TO PLAY AFTER GAME IS OVER (THIS IS AN ERROR)
    letter = random.choice('abcdefghijklmnopqrstuvwxyz')
    response = test_app.put('/api/games/' + game_id, data = json.dumps( dict(letter=letter) ), headers = {'Content-Type': 'application/json', 'Accept': 'application/json'  } ) 
    assert response.status_code == 403, 'post game guesses are forbiddem'

    # DELETE game 
    response = test_app.delete('/api/games/' + game_id)
    assert response.status_code == 200, 'unable to delete game ' + response.status.code


def test_multiple_games(test_app): 
    for i in range(1000):
        test_full_random_game(test_app)


def test_auth(test_app):
    pass