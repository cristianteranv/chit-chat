import React from "react"
import { ListItem } from "./ListItem"

export function List(props){
    const LIs = props.arr.map((item,index) => <ListItem key={index} value={item}/>)
    
    return (
        <ul>
            {LIs}
        </ul>
    )
    
}