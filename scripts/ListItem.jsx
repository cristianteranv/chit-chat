import React from "react"

export function ListItem (props){
    
    return (
        <li>{props.text} sent by: {props.username}</li>
    )
}