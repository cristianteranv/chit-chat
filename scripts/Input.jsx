import * as React from 'react';
import { Socket } from './Socket';

export function Input() {
    
    function onKeyPress (e) {
        if(e.which === 13) {
            document.getElementById("sendButton").click()
        }
    }
    
    return (
        <input id="textInput" type="text" onKeyPress={onKeyPress}/>
    );
}
