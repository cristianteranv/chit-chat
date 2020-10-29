import * as React from 'react'

export function Input (props) {
  // function onKeyPress (e) {
  //     if(e.which === 13) {
  //         document.getElementById("sendButton").click()
  //     }
  // }
  // onKeyPress={onKeyPress}

  return (
        <input id={props.id} type="text" />
  )
}
