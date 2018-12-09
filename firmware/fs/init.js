load('api_gpio.js');
load('api_aws.js');

let pins = {
    "red": 12,
    "yellow": 13,
    "green": 14
};

let state = {
    "red": "off",
    "yellow": "off",
    "green": "off"
};

for (let pinName in pins) {
    GPIO.set_mode(pins[pinName], GPIO.MODE_OUTPUT);
}

function enforceState(newState) {
    for (let pinName in pins) {
        if (newState[pinName] === "on") {
            GPIO.write(pins[pinName], 1);
            state[pinName] = "on";
        } else {
            GPIO.write(pins[pinName], 0);
            state[pinName] = "off";
        }
    }
}

AWS.Shadow.setStateHandler(function(ud, ev, reported, desired) {
    print('event:', ev, '('+AWS.Shadow.eventName(ev)+')');
    if (ev === AWS.Shadow.CONNECTED) {
        AWS.Shadow.update(0, state);
    } else if (ev === AWS.Shadow.UPDATE_DELTA) {
        enforceState(desired);
        AWS.Shadow.update(0, state);
    }
}, null);
