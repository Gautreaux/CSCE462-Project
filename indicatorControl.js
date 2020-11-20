//manages the indicator


// TODO - how should secondary parameter be configured
function setIndicatorGeneric(indicatorRef, property){
    indicatorRef.style.backgroundColor = property;
}

function getInidcatorRefByLabel(indicatorLabel){
    let e = document.getElementById("indicator" + indicatorLabel);
    if(e == undefined){
        throw TypeError("Could not find indicator with label: " + indicatorLabel);
    }
    return e;
}

function setIndicatorPressed(indicatorLabel){
    setIndicatorGeneric(getInidcatorRefByLabel(indicatorLabel), 'green');
}

function setIndicatorReleased(indicatorLabel){
    setIndicatorGeneric(getInidcatorRefByLabel(indicatorLabel), 'red');
}

function setIndicatorSmart(indicatorLabel, value){
    if(value == '+'){
        setIndicatorPressed(indicatorLabel)
    }else{
        setIndicatorReleased(indicatorLabel)
    }
}