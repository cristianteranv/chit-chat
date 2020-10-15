    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';
import { List } from './List'

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [username, setUsername] = React.useState();
    const [count, setCount] = React.useState(0);
    
    function getNewCount() {
        React.useEffect(()=>{
            Socket.on('count', updateCount);
            return () => {
                Socket.off('count', updateCount);
            };
        });
    }
    
    function updateCount(data){
        setCount( data['count'] );
    }
    
    function getUsername() {
        React.useEffect(()=>{
            Socket.on('connected', updateUsername);
            return () => {
                Socket.off('connected', updateUsername);
            };
        });
    }
    
    function updateUsername(data){
        //console.log("Received user name from server: ", data['usrname']);
        setUsername(data['usrname']);
    }
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('messages received', updateAddresses);
            var elem = document.getElementById('chatContainer');
            elem.scrollTop = elem.scrollHeight;
            return () => {
                Socket.off('messages received', updateAddresses);
            };
        });
    }
    
    function updateAddresses(data) {
        //console.log("Received addresses from server: " + data['allMessages']);
        setMessages(data['allMessages']);
    }
    
    getUsername();
    getNewAddresses();
    getNewCount();

    return (
        <div>
            <h1>List of messages:</h1>
            <div>You are: {username}.</div>
            <div>There are {count} users connected.</div>
            <List arr={messages} user={username} />
            <Button username={username} />
        </div>
    );
}
