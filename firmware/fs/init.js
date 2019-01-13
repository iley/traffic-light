load('api_gpio.js');
load('api_aws.js');
load('api_timer.js');

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

function write(pinName, value) {
    GPIO.write(pins[pinName], value);
}

for (let pinName in pins) {
    GPIO.set_mode(pins[pinName], GPIO.MODE_OUTPUT);
}

// Blink all lights on boot.
let booting = true;
for (let pinName in pins) {
    write(pinName, 1);
}

Timer.set(1000, 0, function() {
    booting = false;
    enforceState(state);
}, null);

function enforceState(newState) {
    for (let pinName in pins) {
        if (newState[pinName] === "on") {
            if (!booting) {
                write(pinName, 1);
            }
            state[pinName] = "on";
        } else {
            if (!booting) {
                write(pinName, 0);
            }
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
