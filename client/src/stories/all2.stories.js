import React from 'react';
import {Banner, ResultBanner, UsageAndBlanks} from '../components.js';
import {action} from '@storybook/addon-actions';


export default {
    title: 'Banner and Displays/BannerAndDisplays'
};

export const banner = () => (

    <div>
        <h2> Banner(full)</h2>
        <p> This component includes both Banner and ShortTitle</p>
        <ul>
            <li> full - truthy controlling whether to show title with subtitle</li>
        </ul>
        <h3> Full Title</h3>
        <Banner full= {true}/>
        <h3> Short Title </h3>
        <Banner full= {false}/>
    </div>
);

export const resultBanner = () => (
    <div>
        <h2> ResultBanner</h2>
        <ul>
            <li>  winResult - boolean variable capturing a win or lose</li>
        </ul>
        <h3> win game </h3>
        <ResultBanner winResult= {true}/>
        <h3> loose game </h3>
        <ResultBanner winResult= {false}/>
    </div>
);

export const usageAndBlanks = () => (
    <div>
        <h2> UsageAndBlanks(usage, blanks, showBlanks)</h2>
        <p> The component uses the non-React function prepareUsage</p>
        <ul>
            <li> usage - usage example with guess word as underscores</li>
            <li> blanks - guessed/non-guessed letters, like "sm__t_"</li>
            <li> showBlanks - whether to show blanks seperately or in usage</li>
        </ul>
        <h3> With blanks</h3>
        <UsageAndBlanks
            usage= "The sky loomed dark and ______."
            blanks = "__oo_y"
            showBlanks = {true}
        />

        <h3> Without blanks</h3>
        <UsageAndBlanks
            usage= "The sky loomed dark and ______."
            blanks = "gloomy"
            showBlanks = {false}
        />
    </div>
);
