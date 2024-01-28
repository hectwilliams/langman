import React , {Component, createRef} from 'react';
import styled from 'styled-components';

const GallowCanvas = styled.canvas`
    padding: 10px;
`;

class Gallows extends Component {
    canvasRef = createRef();
    componentDidMount() {  //called after first render cycle (i.e. component has been mounted)
        this.componentDidUpdate(); // invoked after component updates (prevProps,prevState ,  this.props, this.state may be read)
    }
    componentDidUpdate() {

        //  canvas ref via 2d context 
        const ctx = this.canvasRef.current.getContext("2d");
        // render skeleton 
        ctx.fillRect(0, 290, 200, 10);   // base      Note:  x, y, width height --> top left corner being the origin - [0,0]
        ctx.fillRect(20, 0, 10, 300);  // vertical line 
        ctx.fillRect(20, 0,  100, 10 ); // top line 
        ctx.fillRect(120, 0, 10, 40);  // top hook

        
        const badGuesses = this.props.badGuesses;
        
        if (badGuesses >= 1) {
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(125, 75, 30, 0, 2 * Math.PI); // x, y, radius, startAngle, endAngle
            ctx.stroke();
        }
        
        if(badGuesses >= 2) {
            ctx.fillRect(120, 110, 10, 80);
        }
        
        ctx.lineWidth = 6.7;

        if(badGuesses >= 3) {   // arm 1
            ctx.beginPath();
            ctx.moveTo(120, 126);
            ctx.quadraticCurveTo(90, 160, 60, 125);
            ctx.stroke();
        }

        if(badGuesses >= 4) {   // arm 2
            ctx.beginPath();
            ctx.moveTo(130, 126);
            ctx.quadraticCurveTo(160, 160, 190, 135);
            ctx.stroke();
        }

        if(badGuesses >= 5) {   // leg 1
            ctx.beginPath();
            ctx.moveTo(120, 190);
            ctx.quadraticCurveTo(80, 220, 70, 270);
            ctx.stroke();
        }

        if(badGuesses >= 6) {   // leg 2
            ctx.beginPath();
            ctx.moveTo(130, 190);
            ctx.quadraticCurveTo(130, 220, 183, 260);
            ctx.stroke();
        }

    }

    render() {
        return ( 
            <div>
                {/* ref makes component directly accessible using this.refs  */}
                <GallowCanvas ref={this.canvasRef} width={200} height={300 }/>  
            </div>
        );
    }

}

export {Gallows};