

import React, {Component} from 'react';
import {GlobalStyle} from './font';
import {SignInScreen} from './screens';
import axios from 'axios';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      gameStatus: 'logged out'
    };
    this.startGame = this.startGame.bind(this);
  };
  
  startGame(username, lang) {
    const APIURL = 'http://127.0.0.1:5000/'; //server is at port 3000
    console.log(username, lang);
    axios.post(APIURL + 'api/games', {username:username, language:lang}) 
    .then(response => {
      console.log(response);
    })
  };

  
  render() {
    const {gameStatus} = this.state;
    let screen = <>s</>;

    if (gameStatus === 'logged out') {
      const startGame = this.startGame;
      screen = <SignInScreen clickStart={startGame} />;
    } else {
      return <div> Status {gameStatus} </div>;
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
