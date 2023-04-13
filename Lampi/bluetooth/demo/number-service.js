var util = require('util');
var events = require('events');
var bleno = require('bleno');

var CHARACTERISTIC_NAME = 'Some Number';

var NumberCharacteristic = function(deviceState) {
    bleno.Characteristic.call(this, {
        uuid: '7a4b0001-999f-4717-b63a-066e06971f59',
        properties: ['read', 'write', 'notify'],
        descriptors: [
            new bleno.Descriptor({
               uuid: '2901',
               value: CHARACTERISTIC_NAME
            }),
            new bleno.Descriptor({
               uuid: '2904',
               value: new Buffer([0x04, 0x00, 0x27, 0x00, 0x01, 0x00, 0x00])
            }),
        ],
    }
    )

    this.deviceState = deviceState;

    this._update = null;

    this.changed = function(new_value) {
        console.log('updated value - need to Notify?');
        if( this._update !== null ){
            var data = Buffer(1);
            data.writeUInt8(new_value, 0);
            this._update(data);
        }
    }

    this.deviceState.on('changed', this.changed.bind(this));

}

util.inherits(NumberCharacteristic, bleno.Characteristic);

NumberCharacteristic.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest');
    if(offset) {
        callback(this.RESULT_ATTR_NOT_LONG, null);
    } 
    else {
        var data = new Buffer(1);
        data.writeUInt8(this.deviceState.value);
        console.log('onReadRequest returning ', data);
        callback(this.RESULT_SUCCESS, data);
    }
}

NumberCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
    console.log('onWriteRequest');
    if(offset) {
        console.log('onWriteRequest RESULT_ATTR_NOT_LONG');
        callback(this.RESULT_ATTR_NOT_LONG);
    }
    else if (data.length !== 1) {
        console.log('onWriteRequest RESULT_INVALID_ATTRIBUTE_LENGTH');
        callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
    }
    else {
        var new_value = data.readUInt8(0);
        console.log('onWriteRequest ', new_value);
        this.deviceState.set_value( new_value);
        callback(this.RESULT_SUCCESS);
    }
};

NumberCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
    console.log('subscribe on ', CHARACTERISTIC_NAME);
    this._update = updateValueCallback;
}

NumberCharacteristic.prototype.onUnsubscribe = function() {
    console.log('unsubscribe on ', CHARACTERISTIC_NAME);
    this._update = null;
}

function NumberService(deviceState) {
    bleno.PrimaryService.call(this, {
        uuid: '7a4bbfe6-999f-4717-b63a-066e06971f59',
        characteristics: [
            new NumberCharacteristic(deviceState),
        ]
    });
}

util.inherits(NumberService, bleno.PrimaryService);

module.exports = NumberService;

