

import React, {Component} from 'react';
import {GlobalStyle} from './font';
import {SignInScreen, PlayScreen, WinScreen, LoseScreen} from './screens';
import axios from 'axios';

export const APIURL = 'http://127.0.0.1:5000/'; //client at port 3000 (Front End),  server at 5000

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { gameStatus: 'logged out', flashMessage: '', loginToken:''}; //s3cr3t
    this.startGame = this.startGame.bind(this);
    this.guessLetter = this.guessLetter.bind(this);
    this.playAgain = this.playAgain.bind(this);
    this.quitGame = this.quitGame.bind(this);
    // state callbacks 
    this.postGame = this.postGame.bind(this);
    this.getGame = this.getGame.bind(this);
  };

  postGame() {
    if (this.state.loginToken) {
      const {loginToken, language} = this.state;
      axios( { method: 'post', url: APIURL +'api/games', data: {language: language}, headers: {Authorization: 'Bearer' + ' ' + loginToken}} ) // get game token using general token
      .then( response => {
        const {access_token, game_id} = response.data;
        this.setState({gameId: game_id, gameToken: access_token}, this.getGame);
      })
      .catch( err => {
        console.log(err)
        this.setState({flashMessage: 'Failed to start a game' , gameToken: null})
      });
    }
  }

  getGame() {
    axios({method: 'get', url: APIURL + 'api/games/' + this.state.gameId, headers: {Authorization: 'Bearer' + ' ' + this.state.loginToken}}) // get game using game token 
    .then( response =>{
      const {bad_guesses, guessed, player, reveal_word, usage} = response.data; 
      this.setState({badGuesses: bad_guesses, guessed:guessed, playerId: player, revealWord: reveal_word, usage:usage, gameStatus: 'active', flashMessage: ''});
    })
    .catch(err => {
      this.setState({flashMessage: 'Failed to access a new game', gameToken: null});
    });
  }


  startGame(username, passwordValue, registerNewAccount, lang) {
    this.setState ({ username: username, password: passwordValue, language: lang} ) ; // new or active token 
    
    axios( {method: registerNewAccount ? 'post' : 'put', url: APIURL + 'api/auth' , data: {username: username, password: passwordValue}} )
    .then(response => {
      const {access_token} = response.data;       
      const {language} = this.state;
      this.setState ({ username: username, password: passwordValue, language: language, loginToken: access_token} , this.postGame ); 
    })
    .catch(error =>  {
      this.setState({flashMessage : "Account" + ' ' + (registerNewAccount ? "creation" : "login") + ' ' + "failed", loginToken : null}); 
    })
  };

  guessLetter(letter, numCalls=0) {
    const gameId = this.state.gameId;
    axios({method: 'put', url: APIURL + 'api/games/' + gameId, data: {letter}, headers: {Authorization: 'Bearer' + ' ' + this.state.gameToken} })
    .then(response => {
      const {bad_guesses, guessed, reveal_word, result, secret_word} = response.data;
      this.setState({badGuesses: bad_guesses, guessed: guessed, revealWord: reveal_word, gameStatus: result, secretWord: secret_word, flashMessage:''});
    })
    .catch(err => {
      // token expire ?
      if (err.response && (err.response.status === 400)) {
        if (err.response.data.msg === 'User claims verification failed') {
          if (numCalls === 4){
            this.setState({flashMessage: 'Server not accepting credentials'}); 
          } else {
            const {username, password} = this.state;
            axios({method: 'put', url: APIURL + 'api/auth', data: {username: username, password: password} })  // re-login 
            .then(response => {
              // succesful login, update the expired token
              this.setState({loginToken: response.data.access_token});
              axios({method: 'get', url: APIURL + 'api/games/' + this.state.gameId, headers: {Authorization: 'Bearer' + ' ' + this.state.loginToken} }) // GET game using general token 
              .then(response => { 
                this.setState({gameToken: response.data.access_token}); 
              });
            })
            .finally( ()=> {
              // try with a possibly corrected token 
              this.guessLetter(letter, numCalls + 1);
            })
          } 
        }
      } else {
        // all other errors 
        this.setState({flashMessage: 'Server did not recieve your guess'})
      }
    });
  }
  
  playAgain(lang) {
    this.startGame(this.state.username, this.state.password, false, lang);
  }

  quitGame() {
    console.log('quitting')
    this.setState({gameStatus: 'logged out'});
  }

  render() {
    const {gameStatus, flashMessage} = this.state;
    let screen = <></>;
    
    if (gameStatus === 'logged out') {
      const startGame = this.startGame;
      screen = <SignInScreen clickStart={startGame} flashMessage={flashMessage} />;
    } else if (gameStatus === 'active') {
      const {usage, revealWord, guessed, badGuesses} = this.state; 
      const guessLetter = this.guessLetter;
      screen = <PlayScreen usage = {usage} blanks = {revealWord} usedLetters={guessed} numBadGuesses={badGuesses} onGuess={guessLetter} flashMessage={flashMessage} />;
    } else if (gameStatus === 'won') {
      const {language} = this.state;
      const playAgain = this.playAgain;
      const quitGame = this.quitGame;
      screen = <WinScreen lang={language} clickPlayAgain={playAgain} clickQuit={quitGame} />
    } else if (gameStatus === 'lost') {
      const {usage, secretWord, language} = this.state; 
      const playAgain = this.playAgain;
      const quitGame =  this.quitGame; 
      screen = <  LoseScreen usage= {usage} blanks={secretWord} lang={language} clickPlayAgain={playAgain} clickQuit={quitGame} />
    } else {
      screen = <div> Unexpected {gameStatus} </div>
    }

    return (
      <> 
        <GlobalStyle/>
          {screen}
      </>
    ); 
  }
}

export default App;
