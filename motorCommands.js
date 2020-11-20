//functions for interfacing with the motor
var LEFT = 0
var RIGHT = 1
var labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
var activeMovement = null;

//setsup the conroller table
function initalizeControlTable(){
    let indicies = [-1];
    let p = -1;

    let e = document.getElementById("expandingTable");
    let html = e.innerHTML;
    // console.log(html)
    // console.log(p = html.indexOf('_'))

    while((p = html.indexOf('_', p+1)) != -1 ){
        indicies.push(p);
        p+=1;
    }

    e.innerHTML = "";

    // console.log(indicies);
    labels.forEach(function(lbl){
        let s = ""
        let i;
        for(i = 0; i < indicies.length-1; i++){
            s += html.substring(indicies[i]+1, indicies[i+1]) + lbl;
        }
        s += html.substring(indicies[indicies.length-1]+1)
        e.innerHTML += s;
    })
}

//issue a command for motor behavior
function motorStep(motorID, dir, steps){
    let k = ((dir == LEFT)? '-':'+');
    send("M " + motorID + " " + k + " " + steps);
}

function motorContinue(motorID, dir){
    //TODO - speed component
    if(activeMovement != null){
        clearInterval(activeMovement);
    }
    //TODO - workaround?
    //there is some limit on how fast the send can occur
    //interval to call in ms (about .2 rev/sec)
    activeMovement = setInterval(motorStep, 25, motorID, dir, 1);
}

function motorDiscontinue(motorID, dir){
    if(activeMovement != null){
        clearInterval(activeMovement);
        activeMovement = null;
    }
}

function motorEnable(motorID, boxRef){
    send("ENBL " + motorID + " " + ((boxRef.checked)? '+' : '-'));
}

function motorHome(motorID){
    send("HOME " + motorID);
}