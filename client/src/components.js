import React, {Component} from 'react'; 
import styled from 'styled-components';

const TitleFontDiv = styled.div`
    font-family: 'Allura', cursive;
    font-size: 6em;
    :first-letter {
        font-size: 150%;
        margin-right: -0.1em;
    }
    padding-left: 0.2em;
    text-align: left;
`;

const SubTitleDiv = styled.div`
    font-family: 'Allura', cursive;
    font-size: 2em;
    text-align: left;
    margin-top: -2em;
    padding-right: 3em;
`;

const BlockFontDiv = styled.div`
    background-color : ${props => (props.winResult? "#ccc" : "transparent") };
    font-family: 'Passion One' , sans-serif;
    font-size: 4em;
`;

const InUsageSpan = styled.span`
    text-decoration: ${props => props.showBlanks? "none" : "underline"};
    padding-left: 0.3em;
    padding-right: 0.3em;
    display: inline-block;
`;

const BlanksDiv = styled.span`
    letter-spacing: 0.3em;
    font-size : 1.5em;
    text-align: center;
`;

class Banner extends Component {
    render() {
        const {full} = this.props;
        return (
            <div>
                <TitleFontDiv>
                    Lang-Man
                </TitleFontDiv>
                {
                    full && 
                    <SubTitleDiv>
                    play multilingual hangman
                    </SubTitleDiv>
                }
            </div>
        );
    }
}

class ResultBanner extends Component {
    render() {
        const {winResult} = this.props;
        return  (
            <BlockFontDiv>  
                {winResult? "You Won!" : "You Lost" } 
            </BlockFontDiv>
        )
    };
}

function prepareUsage(usage, blanks, showBlanks) {
    const [beforeBlanks, afterBlanks] = usage.split(/_+/)  
    const newBlanks = (showBlanks ? blanks.replace(/./g, '_'): blanks);

    return (
        <p>
            {beforeBlanks}
            <InUsageSpan showBlanks={showBlanks}>
                {newBlanks}
            </InUsageSpan>
            {afterBlanks}
        </p>
    );
}

class UsageAndBanks extends Component {
    render() {
        const {usage, blanks, showBlanks} = this.props;
        const newUsage = prepareUsage(usage, blanks, showBlanks);
        const newBlanks = <BlanksDiv>{blanks}</BlanksDiv>
        
        return (
            <div> 
                {newUsage}
                {showBlanks && newBlanks}
            </div> 
        ); 
            
    }
}


export {Banner, ResultBanner, UsageAndBanks}