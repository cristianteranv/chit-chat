import * as React from 'react'
import { Socket } from './Socket'
import { Input } from './Input'

export function Button (props) {
  function handleSubmit (event) {
    var textInput = document.getElementById('textInput').value
    console.log('handleSubmit.. Received new text from input element: ', textInput)
    console.log("sending",{
      message: textInput,
      usrname: props.username,
      userId: props.userId
    })
    Socket.emit("newMessage", {
      message: textInput,
      usrname: props.username,
      userId: props.userId
    }, ()=>{
      console.log('acknowledge')
    })

    console.log('handleSubmit.. Just emitted message ' + textInput + ' to the server.')
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
