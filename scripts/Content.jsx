    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';
import { List } from './List'

export function Content() {
    const [messages, setMessages] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('new message', updateAddresses);
            return () => {
                Socket.off('messages received', updateAddresses);
            }
        });
    }
    
    function updateAddresses(data) {
        console.log("Received addresses from server: " + data['allAddresses']);
        setMessages(data['allAddresses']);
    }
    
    getNewAddresses();

    return (
        <div>
            <h1>List of messages:</h1>
                <List arr={messages} />
            <Button />
        </div>
    );
}
