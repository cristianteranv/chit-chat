import * as React from 'react'
import { Socket } from './Socket'
import ReactDOM from 'react-dom'
import GoogleLogin from 'react-google-login'

export function GoogleButton (props) {
  const responseGoogle = (response) => {
    console.log('Auth failure. Google response: ', response)
  }

  function handleSubmit (response) {
    // TODO replace with name from oauth
    console.log('Got response:', response)
    Socket.emit('googleAuth', {
      name: response.profileObj.name,
      email: response.profileObj.email,
      uid: response.googleId,
      socketId: props.socketId,
      imgUrl: response.profileObj.imageUrl
    })
  }

  return <GoogleLogin
        clientId="1062054290390-k78ra3cikp1topp72a1s8bo02m965adi.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={handleSubmit}
        onFailure={responseGoogle} /* Runs when auth fails, or auth popup is closed. */
        cookiePolicy={'single_host_origin'}
    />
}
