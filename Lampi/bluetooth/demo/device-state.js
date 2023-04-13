var util = require('util');
var events = require('events');

function DeviceState() {

    this.value = 0;
}

util.inherits(DeviceState, events.EventEmitter);

DeviceState.prototype.set_value = function(new_value) {
    if( this.value != new_value) {
        this.value = new_value % 256;
        this.emit('changed', this.value);
    }
};

module.exports = DeviceState;
