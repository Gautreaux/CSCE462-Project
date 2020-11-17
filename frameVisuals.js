
//manages the behavior on a webpage rescale
function rescaleHandler(){
    k = document.getElementById("frameImage");
    w = k.clientWidth;
    scale = w/1158;

    //TODO Need to update depth too?
    //TODO Scaling factor should be different for the gantry?
    //      because of the gantry size? wider than frame?
    e = document.getElementsByClassName("gantry");
    for (i = 0; i < e.length; i++){
        e[i].style["transform"] = "scale(" + scale + ")";
    }
    e = document.getElementsByClassName("carriage");
    for (i = 0; i < e.length; i++){
        e[i].style["transform"] = "scale(" + scale + ")";
    }

    //TODO - need to maintain position?
}

function positionGantry(elem, depthPct){


    let k = document.getElementById("frameImage");
    let h = k.clientHeight;

    let t = "translateY("+ depthPct +"%)"
    let s = elem.style["transform"]
    let i = s.indexOf("translateY");
    if (i == - 1){
        s = s + " " + t;
    }else{
        let ii = s.indexOf(")", i);
        s = s.substring(0,i) + " " + s.substring(ii+1) + t;
    }

    elem.style["transform"] = s;
}

function positionGantryA(depth){
    if(depth < 0 || depth > 1){
        throw Error("Illegal Axis Depth: " + depth);
    }

    let depthPct = (337-25)*depth+25;
    if(depthPct > 265){depthPct = 265}; //Limit by actual motion
    positionGantry(document.getElementById("gantryA"), depthPct)
}

function positionGantryB(depth){
    if(depth < 0 || depth > 1){
        throw Error("Illegal Axis Depth: " + depth);
    }

    let depthPct = (325-10)*depth+10;
    if(depthPct < 90){depthPct = 90}; //Limit by actual motion
    positionGantry(document.getElementById("gantryB"), depthPct)
}


// function positionCarriage(elem, depthPct, crossPct){

// }