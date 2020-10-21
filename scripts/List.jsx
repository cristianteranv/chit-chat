import React from "react"
import { ListItem } from "./ListItem"

export function List(props){
    const LIs = props.arr.map((item, index) => {
        if (props.userId == item['userId']){
            return <ListItem key={index} text={item['message']} date={item['date']} username={item['username']} styleClass="mine message"/>
        }
        else if (item['username'] == "jokebot"){
            return <ListItem key={index} text={item['message']} date={item['date']} username={item['username']} styleClass="jokebot message"/>
        }
        else{
            return <ListItem key={index} text={item['message']} date={item['date']} username={item['username']} imgUrl={item['imgUrl']} styleClass="yours message"/>
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