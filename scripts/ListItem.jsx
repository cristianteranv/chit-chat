import React from "react"

export function ListItem (props){
    
    return (
        <div className="messages">
            <div className={props.styleClass}>
                <div>Sent by: {props.username}. Style: {props.styleClass}</div>
                <div>{props.text}</div>
            </div>
        </div>
    )
}