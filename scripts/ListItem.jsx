import React from "react";
import Linkify from 'react-linkify';

export function ListItem (props){
    
    // {props.imgUrl?
    //         <img src={props.imgUrl}/>
    //         :<div>NI</div>
    //         }
    
    
    return (
        <div className="messages">
            <div className={props.styleClass}>
                <div>Sent by: {props.username}. Style: {props.styleClass}</div>
                <Linkify><div>{props.text}</div></Linkify>
            </div>
        </div>
    )
}