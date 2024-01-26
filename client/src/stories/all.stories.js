import React from 'react';
import {LetterButton, ButtonPanel, StartForm, PlayAgainPanel} from '../buttons.js';

import {action} from '@storybook/addon-actions';
// import { addDecorator } from '@storybook/react';
// import { GlobalStyle } from '../font.js';

// addDecorator( s =>  <>
//                         <GlobalStyle/> 
//                         { s() }
//                     </>
// );

export default {
    title: 'Button-related Components/Button',
    // parameters: {
    //   layout: 'centered',
    // },
    // tags: ['autodocs'],
    // argTypes: {},
};

export const letterButton = () => (
    <div>
        <h2> LetterButton(letter, wasUsed, makeGuess) </h2>
        <ul>
            <li> letter - the button text, assumed to be one character </li>
            <li> wasUsed - (Boolean) whether the button was used; affects styling </li>
            <li> makeGuess - CallBack to use on button click  </li>
        </ul>
        <h3> Already used </h3>
        <LetterButton letter = "A" wasUsed={true} makeGuess={action('click-A')}  />
        <h3> Not yet used </h3>
        <LetterButton letter = "B" wasUsed={false} makeGuess={action('click-B')}  />
    </div>
);
letterButton.args = {
    label: 'LetterButton',
}

export const buttonPanel = () => (
    <div>
        <h2> ButtonPanel() </h2>
        <ul>
            <li> usedLetters - guessed letters </li>
            <li> onGuess - callback taking the guessed letter </li>

        </ul>
        <h3> two characters guessed</h3>
        <ButtonPanel usedLetters = {"ab"}  onGuess={action("key")} />;
        <h3> three characters guessed</h3>
        <ButtonPanel usedLetters = {"abz"}  onGuess={ action("key")  } />;
    </div>
) 
buttonPanel.args = {
    label: 'buttonPanel',
}

export const startForm = () => (
    <div>
        <h2> StartForm</h2>
        <ul>
            <li> clickStart - gamestart callback -- requires name and language  </li>
        </ul>
        < StartForm clickStart ={action("key")} />
    </div>
)
startForm.args = {
    label: 'startForm',
}

export const playAgainPanel = () => (
    <div>
        <h2> PlayAgainPanel</h2>
        <ul>
            <li>  clickPlayAgain - callback handle new language selection </li>
            <li>  lang - new language  </li>
            <li>  clickQuit - callback to quit playing   </li>
        </ul>
        <PlayAgainPanel clickPlayAgain={action('play-again')} clickQuit={action('key')} />
    </div>

)
playAgainPanel.args = {
    label: 'playAgainPanel',
}