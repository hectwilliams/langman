import { screen } from '@storybook/test';
import React, {Component} from 'react'; 
import styled from 'styled-components';

const images = require.context('../public/icons/', true);
const imageList = images.keys().map(image => images(image));

const zipImageContext = imageList.reduce( (acc, imageId, index) => {
    let file = images.keys()[index].slice(2, -4);
    acc[file] = imageId
    return acc;
}, {} )

// images.keys().map( (ele, index) => {
//     return [ { imgFilename: ele,  imgId: imageList[index] } ];
// });

/*
    top 
        column of link 
    
    bottom 
        left 
            top 
                icon 
            bottom 
                copy right message 

        right 
            row of social media 
*/

const Anchor = styled.a`
    color: inherit; 
`

const BaseItemDiv = styled.div`
    font-family: 'IBM Plex Mono', monospace;
    margin-left: 0;
`


const BaseCols = styled.div`
    display: grid;
    grid-template-columns: repeat(8, 1fr); // 1/8 of page
    grid-column-start: ${prop => (`${prop.test} / span 1` ) } ;
    font-size: 15px;
    padding-bottom: 8em;
    margin : 0 0 0 1em ;

`
const UnorderedList = styled.ul`
    margin-top: 4px;
    padding-left: 0;
    list-style-type: none;
`

const List = styled.li`
    font-size: 10px;
    margin-top: 2px;
`

const Label = styled.label`
    font-weight: bold;
    color: black;
`

class ColumnPanel extends Component {
    render() {
        return (
            <BaseCols>
                <BaseItemDiv test={1}>
                    <Label>Developer </Label>
                    <UnorderedList> 
                        <List> <Anchor href="https://create-react-app.dev/">React</Anchor>  </List>
                        <List> <Anchor href="https://github.com/hectwilliams/langman">Github Repo</Anchor>  </List>
                    </UnorderedList>
                </BaseItemDiv>
                 
                <BaseItemDiv test={2}>
                    <Label>Other</Label>
                    <UnorderedList> 
                        <List> <Anchor href="https://cats.com/">Cats</Anchor>  </List>
                        <List> <Anchor href="https://www.allaboutbirds.org/cams/">All About Birds</Anchor>  </List>
                    </UnorderedList>
                </BaseItemDiv>
            </BaseCols>
        )
    }
}


const DivParition = styled.div`
    display: grid;
    grid-template-columns: repeat(20, 1fr); // 1/20 of page
    grid-column-start: ${prop => (`${prop.test} / span 1` ) } ;
    font-size: 15px;
    margin : 0 0 0 1em ;

`;

const Img = styled.img`
    width: 25px;
    height: 25px;
`;

const ImgIconLeft = styled(Img)`
    width: 30px;
    height: 30px;
`


class IconPanel extends Component {
    render() {
        let screen = [...Array(20).keys() ].map( (_, index) =>  {
            
            if (index == 0)
                return (<ImgIconLeft  src={zipImageContext.hang} /> )
            
            if (index > 0 && index < 16) {
                return  <div></div>
            }
            
            if (index == 16) {
                return (<Img  src={zipImageContext.meta} /> )
            }
            
            if (index == 17) {
                return (<Img  src={zipImageContext.x} /> )
            }
            
            if (index == 18) {
                return (<Img  src={zipImageContext.youtube} /> )
            }
            
            if (index == 19) {
                return (<Img  src={zipImageContext.tiktok} /> )
            }

        }
    ) 
        

        return (
            <DivParition>
                {screen}            
            </DivParition>
        )
    }
}


const Misc =  styled.div`
    display: grid;
    // grid-column: 2 / 4;
    // grid-row: 2 / 4;

`
const DivStatment = styled.div`
    font-family: "Roboto";
    display: block;
    margin : 0 0 0 1em ;

`
const SpanBlock = styled.span`
    // border: 1px solid;
    font-size: 10px;
    padding: 5px 4px 5px 0;
`

const Copyright = styled.div`
    font-size: 10px; 
    text-align: left; 
    margin : 0 0 0 1em ;

    `
const CopyrightParagraph = styled.div`
    margin: 0 0 0 0 ;
    paddomg: 0 0 0 0 ;

`

class CopyrightPanel extends Component {
    render() {
        let tags = ["Privary Policy", "Terms of Us", "Privary Policy",  "Cookie Settings" ,  "About"]

        return (
            <Misc>
                <DivStatment>
                    { tags.map( (dummyTag) => ( <SpanBlock>  <Anchor href="url"> {dummyTag} </Anchor> </SpanBlock>))}
                </DivStatment>
                <br/>
                <Copyright>
                    <CopyrightParagraph> © 2024 Hectron-Capsule Corp.</CopyrightParagraph>
                    <CopyrightParagraph> Hectron Affliates</CopyrightParagraph>
                </Copyright>
                
            </Misc>
        )
    }
}

export {ColumnPanel, IconPanel, CopyrightPanel};
