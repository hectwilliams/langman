import React, {Component} from 'react'; 
import styled from 'styled-components';

// const BaseLetterButton = styled.button`
//     font-size: 36px;
//     padding: 2px;
//     margin: auto;
//     border-radius: 13px;
//     width: 1em;
//     background-color: #eee;
// `;

// const UsedLetterButton = styled(BaseLetterButton)`
//     background-color: #777;
//     margin: 2px
// `;

// const UnusedLetterButton = styled(BaseLetterButton)`
//     background-color: #ccc;
//     margin: 2px;
//     &:hover {
//         background-color: #eee;
//     }
// `;

const BaseLetterButton = styled.button`
    font-family: 'IBM Plex Mono', monospace;
    font-size: 30px;
    padding: 0em 0.9em 1.3em 0.3em;
    margin: 0.1em;
    border-radius: 0.5em;
    text-align: center;
    width: 1em;
    height: 1.2em;
    background-color: ${ props => (props.used ? "#777" : "#ccc" )};
    &:hover {
        ${ props=> props.used ? "" : "background-color: #eee;" }
    };
`;

const BoxPanel = styled.div`
    display: inline-block;
    font-size: 30px;
    background-color: #444;
    color: #fff;
    border-radius: 26px;
    padding: 20px;
    margin: 10px;
`;

const FormInput = styled.input`
    padding: 3px;
    margin: 6px;
    text-align: center;
    font-family: inherit;
`;

const FormSelect = styled.select`
    padding: 3px;
    margin: 6px;
    text-align: center;
    font-family: inherit;
`;


class LetterButton extends Component {
    render() {
        const {letter, wasUsed, makeGuess} = this.props;
        return (
            < BaseLetterButton used={wasUsed} onClick={wasUsed? null : makeGuess} >
                {letter}
            </ BaseLetterButton >
        );
    }
}



const _alphabet = () => {
    const arr = [];
    for (let i = 65; i <= 90; i++) {
        arr.push(String.fromCharCode(i));
    }
    return arr;
}

class ButtonPanel extends Component {
    alphabet = _alphabet();

    makeGuess(letter) {
        return () => {
            this.props.onGuess(letter);
        }
    }

    constructor (props) {
        super(props);
        this.makeGuess = this.makeGuess.bind(this);
    }

    render() {
        const usedLetters = this.props.usedLetters.toUpperCase()
        const letterButtons = this.alphabet.map( (letter) => {
                return  <LetterButton key={letter} letter={letter}  wasUsed={usedLetters.includes(letter)} makeGuess={this.makeGuess(letter)}  />;
            }
        );
        
        return(
            <BoxPanel>
                {letterButtons}
            </BoxPanel>
        );
    }
}

class StartForm extends Component {
    render() {
        return <div>  Start Form </div>
    }
}

class PlayAgainPanel extends Component {
    render () {
        return <div> Play Again Panel </div>
    }
}

export {LetterButton, ButtonPanel, StartForm, PlayAgainPanel};