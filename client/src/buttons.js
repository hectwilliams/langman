import React, {Component} from 'react'; 
import styled from 'styled-components';

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
    padding: 3px;
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
    alphabet = _alphabet(); 

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
        this.state = { nameValue: "", langValue: "en", registerNewAccount: false, passwordValue: "" };
        this.onNameChange = this.onNameChange.bind(this);
        this.onLangChange = this.onLangChange.bind(this);
        this.onPasswordChange = this.onPasswordChange.bind(this);
        this.clickWrapper = this.clickWrapper.bind(this);
        this.onNewAccountChange = this.onNewAccountChange.bind(this);
    }

    onNameChange(event) {
        this.setState({nameValue: event.target.value});
    }

    onLangChange(event) {
        this.setState({langValue: event.target.value});
    }

    onPasswordChange(event) {
        this.setState({passwordValue: event.target.value})
    }

    onNewAccountChange(event) {
        this.setState({registerNewAccount: event.target.checked})
    }

    clickWrapper() {
        const {nameValue, langValue, passwordValue, registerNewAccount} = this.state; // read nameValue and langValue from this.state object 
        this.props.clickStart(nameValue, passwordValue, registerNewAccount, langValue);
    }

    render() {
        const  {clickWrapper, onNameChange, onLangChange, onPasswordChange, onNewAccountChange} = this;
        const {nameValue, passwordValue, registerNewAccount,langValue} = this.state; 
        return (
            <div>
                <form>
                    <label htmlFor="nameInput"> Enter your name </label>
                    <FormInputStyle value={nameValue} type="text" name="name" onChange={onNameChange}  /> 
                    <br/> 
                    <label htmlfor="password"> Password</label>
                    <FormInputStyle value = {passwordValue} type={"password"} name={"password"} onChange={onPasswordChange} /> 
                    <br/> 
                    Register new account?&nbsp;
                    <FormInputStyle checked={registerNewAccount} type={"checkbox"} onChange={onNewAccountChange} />
                    <br/>
                    <label htmlFor='languageInput'> Choose a Language </label>
                    <FormSelectStyle onChange={onLangChange} value={langValue} id="languageInput" name="language" >
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                    </FormSelectStyle>
                    <br/>
                    <ActionButtonStyle type="button" onClick={clickWrapper}>
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
        this.state = {langValue: props.lang};
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
                        <option value="en" >English</option>
                        <option value="fr" >French</option>
                        <option value="es" >Spanish</option>
                    </FormSelectStyle>
                    <ActionButtonStyle type="button" onClick={clickWrapper}>
                        Play Again
                    </ActionButtonStyle>
                    <ActionButtonStyle type="button" onClick={clickQuit}>
                        Quit
                    </ActionButtonStyle>
                </form>
            </div>
        )   
     }
}

export {LetterButton, ButtonPanel, StartForm, PlayAgainPanel};

