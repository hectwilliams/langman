

import React, {Component} from 'react';
import {GlobalStyle} from './font';
import {SignInScreen, PlayScreen, WinScreen, LoseScreen} from './screens';
import axios from 'axios';

const APIURL = 'http://127.0.0.1:5000/'; //server is at port 3000

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      gameStatus: 'logged out'
    };
    this.startGame = this.startGame.bind(this);
    this.guessLetter = this.guessLetter.bind(this);
  };
  
  startGame(username, lang) {
    console.log(username, lang);
    
    axios.post(APIURL + 'api/games', {username:username, language:lang}) 
      .then(response => {
        if (response.data.message === 'success' ) {
          const gameId = response.data.game_id;
          this.setState ({username: username, language: lang, gameId: gameId});
          axios.get(APIURL + `api/games/${gameId}`)
          .then(response => {
            this.setState({badGuesses: response.data.bad_guesses, guessed: response.data.guessed, playerId: response.data.player, revealWord: response.data.reveal_word, usage: response.data.usage, gameStatus: 'active' });
          })
          .catch(err => {alert('Ooops. Server not responsive')});
        }
      })
    .catch(err  => alert('Oops. server not responsive'));
  };

  guessLetter(letter) {
    const gameId = this.state.gameId;
    axios.put(APIURL + `api/games/${gameId}`, {letter})
    .then(response => {
      this.setState({
        badGuesses: response.data.badGuesses, 
        guessed: response.data.guessed, 
        revealWord: response.data.reveal_word, 
        gameStatus: response.data.result,
        secretWord: response.data.secret_word
      })
      console.log(response.data)
    });
  }
  
  playAgain(lang) {
    this.startGame(this.state.username, lang);
  }

  quitGame() {
    this.setState({gameStatus: 'logged out'});
  }

  render() {
    const {gameStatus} = this.state;
    let screen = <></>;

    if (gameStatus === 'logged out') {
      const startGame = this.startGame;
      screen = <SignInScreen clickStart={startGame} />;
    } else if (gameStatus === 'active') {
      const {usage, revealWord, guessed, badGuesses} = this.state; 
      const guessLetter = this.guessLetter;
      screen = <PlayScreen usage = {usage} blanks = {revealWord} usedLetters={guessed} numBadGuesses={badGuesses} onGuess={guessLetter}/>;
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
