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

const BaseLetterButtonStyle = styled.button`
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

const BoxPanelStyle = styled.div`
    display: inline-block;
    font-size: 30px;
    background-color: #444;
    color: #fff;
    border-radius: 26px;
    padding: 20px;
    margin: 10px;
`;

const FormInputStyle = styled.input`
    padding: 3px;
    margin: 6px;
    text-align: center;
    font-family: inherit;
`;

const FormSelectStyle = styled.select`
    padding: 3px;
    margin: 6px;
    text-align: center;
    font-family: inherit;
`;

const ActionButtonStyle = styled.button`
    padding: 5px;
    margin: 3px;
    background-color: #ccc;
    font-size: 110%;
    font-family: inherit;
`; 


class LetterButton extends Component {
    render() {
        const {letter, wasUsed, makeGuess} = this.props;
        return (
            < BaseLetterButtonStyle used={wasUsed} onClick={wasUsed? null : makeGuess} >
                {letter}
            </ BaseLetterButtonStyle >
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
    alphabet = _alphabet(); // class property
  

    constructor (props) {
        super(props);
        this.makeGuess = this.makeGuess.bind(this);
    }

    makeGuess(letter) { // class method 
        return () => {
            this.props.onGuess(letter);
        }
    }

    render() {
        // local render variables 
        const usedLetters = this.props.usedLetters.toUpperCase() // this.props properties are inputs to component call 
        const letterButtons = this.alphabet.map( (letter) => {
                return  <LetterButton key={letter} letter={letter}  wasUsed={usedLetters.includes(letter)} makeGuess={this.makeGuess(letter)}  />;
            }
        );
        
        return(
            <BoxPanelStyle>
                {letterButtons}
            </BoxPanelStyle>
        );
    }
}

class StartForm extends Component {
    constructor(props) {
        super(props);
        this.state = {nameValue: "", langValue: "en"};
        this.onNameChange = this.onNameChange.bind(this);
        this.onLangChange = this.onLangChange.bind(this);
        this.clickWrapper = this.clickWrapper.bind(this);
    }

    onNameChange(event) {
        this.setState({nameValue: event.target.value});
    }

    onLangChange(event) {
        this.setState({langValue: event.target.value});
    }

    clickWrapper() {
        const {nameValue, langValue} = this.state; // read nameValue and langValue from this.state object 
        this.props.clickStart(nameValue, langValue);
    }

    render() {
        const  {clickWrapper, onNameChange, onLangChange} = this;
        const {nameValue, langValue} = this.state; 
        return (
            <div>
                <form>
                    <label htmlFor="nameInput"> Enter your name </label>
                    <FormInputStyle value={nameValue} type="text" name="name" onChange={onNameChange}  /> 
                    <br/> 
                    <label htmlFor='languageInput'> Choose a Language </label>
                    <FormSelectStyle onChange={onLangChange} value={langValue} id="languageInput" name="language" >
                        <option>English</option>
                        <option>French</option>
                        <option>Spanish</option>
                    </FormSelectStyle>
                    <br/>
                    <ActionButtonStyle type="button" onclick={clickWrapper}>
                        Start a Game
                    </ActionButtonStyle>
                </form>
            </div>
        )
    }
}

class PlayAgainPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {langValue: "en"};
        this.onLangChange = this.onLangChange.bind(this);
        this.clickWrapper = this.clickWrapper.bind(this);
    }
    
    onLangChange(event) {
        this.setState({langValue: event.target.value});
    }

    clickWrapper() {
        const {langValue} = this.state; // read nameValue and langValue from this.state object 
        this.props.clickPlayAgain(langValue);
    }

    render () {
        const {langValue} = this.state;
        const {clickWrapper , onLangChange} = this;
        const {clickQuit} = this.props; 
        return (
            <div>
                <form>
                    <label htmlFor='languageInput'> Choose a Language </label>
                    <FormSelectStyle onChange={onLangChange} value={langValue} id="languageInput" name="language" >
                        <option>English</option>
                        <option>French</option>
                        <option>Spanish</option>
                    </FormSelectStyle>
                    <br/>
                    <ActionButtonStyle type="button" onclick={clickWrapper}>
                        Play Again
                    </ActionButtonStyle>
                    <ActionButtonStyle type="button" onclick={clickQuit}>
                        Quit
                    </ActionButtonStyle>
                </form>
            </div>
        )   
     }
}

export {LetterButton, ButtonPanel, StartForm, PlayAgainPanel};