
import * as React from 'react'

import { Button } from './Button'
import { Socket } from './Socket'
import { List } from './List'
import { GoogleButton } from './GoogleButton'

export function Content () {
  const [messages, setMessages] = React.useState([])
  const [socketId, setSocketId] = React.useState()
  const [count, setCount] = React.useState()
  const [username, setUsername] = React.useState()
  const [userId, setUserId] = React.useState()
  const [isLoggedIn, setLogin] = React.useState(false)

  function getNewCount () {
    React.useEffect(() => {
      Socket.on('count', updateCount)
      return () => {
        Socket.off('count', updateCount)
      }
    })
  }

  function updateCount (data) {
    setCount(data.count)
  }

  function getUsername () {
    React.useEffect(() => {
      Socket.on('send username', updateUsername)
      return () => {
        Socket.off('send username', updateUsername)
      }
    })
  }

  function updateUsername (data) {
    setUsername(data.username)
    setUserId(data.userId)
    setLogin(true)
  }

  function getSocketId () {
    React.useEffect(() => {
      Socket.on('connected', updateSocketId)
      return () => {
        Socket.off('connected', updateSocketId)
      }
    })
  }

  function updateSocketId (data) {
    // console.log("Received user name from server: ", data['usrname']);
    setSocketId(data.socketId)
  }

  function getNewAddresses () {
    React.useEffect(() => {
      Socket.on('messages received', updateAddresses)
      var elem = document.getElementById('chatContainer')
      elem.scrollTop = elem.scrollHeight
      return () => {
        Socket.off('messages received', updateAddresses)
      }
    })
  }

  function updateAddresses (data) {
    // console.log("Received addresses from server: " + data['allMessages']);
    setMessages(data.allMessages)
  }

  getSocketId()
  getNewAddresses()
  getNewCount()
  getUsername()

  return (
        <div>
            <div>There are {count} users connected.</div>
            <List arr={messages} user={username} userId={userId} />
            {isLoggedIn
              ? <Button username={username} userId={userId} />
              : <div><h1>You need to log in before you can chat!</h1><GoogleButton socketId={socketId} /></div>
            }
        </div>
  )
}
