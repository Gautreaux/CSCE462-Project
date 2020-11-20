
//send the message from the client to the machine
function sendTestMessage(){
    let e = document.getElementById("testMessageInput")
    send("ECHO " + e.value)
}

//connect to user specified server
function manualConnection(){
    let path = document.getElementById("manualConnection").value;

    if(path.length == 0 || path.indexOf(':') == -1){
        //TODO - make more apparent on the screen?
        console.log("Invalid path construction.");
        return;
    }

    let i = path.indexOf("ws://");
    if(i == -1){
        path = "ws://" + path;
    }
    else if( i != 0){
        //TODO - make more apparent on the screen?
        console.log("Invalid path, protocol cannot appear mid path.")
        return;
    }

    console.log("Manual connection path ok with: " + path)

    connect(path)
}