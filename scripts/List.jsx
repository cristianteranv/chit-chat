import React from "react"
import { ListItem } from "./ListItem"

export function List(props){
    const LIs = props.arr.map((item, index) => <ListItem key={index} text={item['message']} username={item['usrname']}/>)
    
    return (
        <ul>
            {LIs}
        </ul>
    )
    
}