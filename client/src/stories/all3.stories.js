import {Gallows} from '../gallows.js';
import {action} from '@storybook/addon-actions';

export default {
    title: "Gallows/GallowDescription"
};

export const gallow = () => (

    <div>
        <h2> Gallows(badGuesses) </h2>
        <ul>
            <li> badGuesses - number ( 0 - 6 ) of parts to draw</li>
        </ul>
        <h3> 6 bad guesses </h3>
        <Gallows badGuesses= {6} />
        <h3> 5 bad guesses </h3>
        <Gallows badGuesses= {5} />
        <h3> 4 bad guesses </h3>
        <Gallows badGuesses= {4} />
        <h3> 3 bad guesses </h3>
        <Gallows badGuesses= {3} />
        <h3> 2 bad guesses </h3>
        <Gallows badGuesses= {2} />
        <h3> 1 bad guesses </h3>
        <Gallows badGuesses= {1} />
        <h3> 0 bad guesses </h3>
        <Gallows badGuesses= {0} />
    </div>

);

