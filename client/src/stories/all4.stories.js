import { SignInScreen, WinScreen, LoseScreen, PlayScreen, FooterScreen } from "../screens";
import {action} from '@storybook/addon-actions';

export default {
    title: "Screens/SignInScreen"
};

export const signinscreen = () => (

    <div>
        <h2>SignInScreen(clickStart)</h2>
        <ul>
            <li> clickStart - callback sending post(name, language) request to server  </li>
        </ul>
        <SignInScreen clickStart={action('start-game')} /> 
    </div>
);

export const winscreen = () => (

    <div>
        <h2>WinScreen(lang, clickPlayAgain, clickQuit)</h2>
        <ul>
            <li> lang - language games played support </li>
            <li> clickPlayAgain - callback setting up a new game</li>
            <li> clickQuit - callback stopping game</li>
        </ul>
        <h3> Expect English</h3>
        <WinScreen lang="en" clickPlayAgain={action("play-again")}  clickQuit={action("quit") } />
        <h3> Expect Spanish</h3> 
        <WinScreen lang="es" clickPlayAgain={action("play-again")}  clickQuit={action("quit") } /> 

    </div>
);


export const losescreen = () => (

    <div>
        <h2>LoseScreen(usage, blanks, lang, clickPlayAgain, clickQuit)</h2>
        <ul>
            <li> usage - usage from game just ended </li>
            <li> blanks - the word to be guessed for ended game </li>
            <li> lang - language of last game played </li>
            <li> clickPlayAgain - callback for a new game using language</li>
            <li> clickQuit - callback stopping game</li>
        </ul>
        <h3> Expect English</h3>
        <LoseScreen  usage={"whom the bell _____, it tools for thee."} blanks = {"tolls"} lang="en" clickPlayAgain={action("play-again")}  clickQuit={action("quit") } />
        
        <h3> Expect Spanish</h3> 
        <LoseScreen usage={"Los _________ nunca abandonan"}  blanks={"ganadores"} lang="es" clickPlayAgain={action("play-again")}  clickQuit={action("quit") } /> 

    </div>
);

export const playscreen = () => (

    <div>
        <h2>LoseScreen(usage, blanks, lang, clickPlayAgain, clickQuit)</h2>
        <ul>
            <li> usage - usage provided as a clue </li>
            <li> blanks - blanks and right guesses  </li>
            <li> usedGuesses - string of letters that have been guessed </li>
            <li> numBadGuesses - integer number of incorrect guesses</li>
            <li> onGuess - callback to use when guessing letter</li>
        </ul>
        <h3>  Typical Game</h3>
        <PlayScreen usage = {"unhappy ______ is unhappy"} blanks={"_a____"} usedLetters="acr" numBadGuesses={2} onGuess={action('guess')} />

    </div>
);

export const footscreen = () => (
    <div>
        <h2> footer for langman</h2>
        <br/>
        <FooterScreen/>
    </div>
);