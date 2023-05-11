import * as React from 'react'
import { Socket } from './Socket'
import { Input } from './Input'

export function Button (props) {
  function handleSubmit (event) {
    var textInput = document.getElementById('textInput').value
    Socket.emit("new msg", {
      message: textInput,
      usrname: props.username,
      userId: props.userId
    })
    document.getElementById('textInput').value = ''
    event.preventDefault()
  }

  return (
        <form onSubmit={handleSubmit}>
            <Input id="textInput"/>
            <button id="sendButton">Send</button>
        </form>
  )
}
