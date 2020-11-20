
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

function genericHTMLExpansion(id_container, expansion_set, expansion_char){
    let indicies = [-1];
    let p = -1;

    let e = document.getElementById(id_container);
    let html = e.innerHTML;

    while((p = html.indexOf(expansion_char, p+1)) != -1 ){
        indicies.push(p);
        p+=1;
    }

    e.innerHTML = "";

    // console.log(indicies);
    expansion_set.forEach(function(lbl){
        let s = ""
        let i;
        for(i = 0; i < indicies.length-1; i++){
            s += html.substring(indicies[i]+1, indicies[i+1]) + lbl;
        }
        s += html.substring(indicies[indicies.length-1]+1)
        e.innerHTML += s;
    })
}