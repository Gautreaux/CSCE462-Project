//functions for interfacing with the motor
var LEFT = 0
var RIGHT = 1
var labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
var activeMovement = null;


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