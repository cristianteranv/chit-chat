import React from "react";
import Linkify from 'react-linkify';

export function ListItem (props){
    
    {props.imgUrl?
            <img src={props.imgUrl}/>
            :<div>NI</div>
            }
    var text = props.text;
    var ext = text.slice(-4);
    if (ext == ".jpg" || ext == ".png" || ext == ".gif"){
        console.log("extension type", ext);
        var imageTag = <img src={text} className="inlineImage"/>
    }
    
    return (
        <div className="messages">
            {props.imgUrl?
            <img src={props.imgUrl} className="profilePic"/>
            :null
            }
            <div className={props.styleClass}>
                <div>Sent by: {props.username}. Style: {props.styleClass}</div>
                <Linkify><div>{imageTag}</div><div>{props.text}</div></Linkify>
            </div>
        </div>
    )
}