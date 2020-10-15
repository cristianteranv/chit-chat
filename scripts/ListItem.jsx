import React from "react"

export function ListItem (props){
    
    return (
        <div className="messages">
            <div className={props.styleClass}>
                {props.text} sent by: {props.username}. Owner: {props.styleClass}
            </div>
        </div>
    )
}