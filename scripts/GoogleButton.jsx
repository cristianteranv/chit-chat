import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';
 

export function GoogleButton(props) {
    const responseGoogle = (response) => {
      console.log("responseGoogle: ", response);
    }
  
    function handleSubmit(response) {
        // TODO replace with name from oauth
        console.log("Reached handle submit", response)
        console.log("name?: ", response.nt.Ad)
        console.log("email?: ", response.nt.Wt)
        console.log("googleId?: ", response.googleId)
        Socket.emit('googleAuth', { //send google unique id
            'name': response.nt.Ad,
            'email': response.nt.Wt,
            'uid': response.googleId,
            'socketId': props.socketId,
            'imgUrl': response.nt.JJ
        });
        
        console.log('Sent the name, email, and authType to server!');
    }

    return <GoogleLogin
        clientId="1062054290390-k78ra3cikp1topp72a1s8bo02m965adi.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={handleSubmit}
        onFailure={responseGoogle} /*Runs when auth fails, or auth popup is closed.*/
        cookiePolicy={'single_host_origin'}
    />
}
