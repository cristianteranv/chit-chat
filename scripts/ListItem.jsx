import React from "react";
import Linkify from 'react-linkify';

export function ListItem (props){
    var text = props.text;
    var ext = text.slice(-4);
    if (ext == ".jpg" || ext == ".png" || ext == ".gif"){
        console.log("extension type", ext);
        var imageTag = <img src={text} className="inlineImage"/>;
    }
    var date = new Date(props.date);
    var offset = date.getTimezoneOffset() / 60;
    date.setHours(date.getHours()-offset);
    date = `${date.getMonth()+1}/${date.getDate()}, ${date.getHours()}:${date.getMinutes()}`;
    
    return (
        <div className="messages">
            {props.imgUrl?
            <img src={props.imgUrl} className="profilePic"/>
            :null
            }
            <div className={props.styleClass}>
                <div className="nameStyle"><b>{props.username}</b></div>
                <Linkify>
                {imageTag?
                <div>{imageTag}</div>
                :null
                }
                <div>{props.text}</div>
                </Linkify>
                <div className="date">{date}</div>
            </div>
        </div>
    );
}