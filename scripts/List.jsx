import React from "react"
import { ListItem } from "./ListItem"

export function List(props){
    const LIs = props.arr.map((item, index) => {
        if (props.userId == item['userId']){
            return <ListItem key={index} text={item['message']} username={item['username']} styleClass="mine message"/>
        }
        else if (item['usrname'] == "jokebot"){
            return <ListItem key={index} text={item['message']} username={item['username']} styleClass="jokebot message"/>
        }
        else{
            return <ListItem key={index} text={item['message']} username={item['username']} styleClass="yours message"/>
        }
    })
    
    // var scrolled = false;
    // function updateScroll(){
    //     if(!scrolled){
    //         var element = document.getElementById("chatContainer");
    //         console.log(element);
    //         element.scrollTop = element.scrollHeight;
    //     }
    // }
    
    // function setScroll(){
    //     scrolled = true;
    // }
    
    // updateScroll();
    
    return (
        <div className="chat" id="chatContainer" >
            {LIs}
        </div>
    )
    
}