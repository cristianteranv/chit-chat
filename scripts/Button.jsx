import * as React from 'react';
import { Socket } from './Socket';
import { Input } from './Input';

function handleSubmit(event) {
    var textInput = document.getElementById("textInput").value
    console.log('handleSubmit.. Received new text from input element: ', textInput);
    
    Socket.emit('new message', {
        'message': textInput,
    });
    
    console.log('handleSubmit.. Just emitted grocery' + textInput + ' to the server.');
    document.getElementById("textInput").value = ""
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <Input id="sendButton" placeholder="Your message here.."/>
            <button>Send</button>
        </form>
    );
}
