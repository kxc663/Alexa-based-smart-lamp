var child_process = require('child_process');
var device_id = child_process.execSync('cat /sys/class/net/eth0/address | sed s/://g').toString().replace(/\n$/, '');

process.env['BLENO_DEVICE_NAME'] = 'LAMPI ' + device_id;

var bleno = require('bleno');

var DeviceInfoService = require('./device-info-service');

var DeviceState = require('./device-state');
var NumberService = require('./number-service');

var deviceState = new DeviceState();

var deviceInfoService = new DeviceInfoService( 'CWRU', 'LAMPI', '123456');
var numberService = new NumberService(deviceState);

deviceState.on('changed', function(new_value) {
    console.log('changed:  value = %d', new_value);
});

setInterval( function() {deviceState.set_value(deviceState.value +1)}, 1000);

bleno.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    bleno.startAdvertising('MyService', [numberService.uuid, deviceInfoService.uuid], function(err)  {
      if (err) {
        console.log(err);
      }
    });
  }
  else {
    bleno.stopAdvertising();
    console.log('not poweredOn');
  }
});

bleno.on('advertisingStart', function(err) {
  if (!err) {
    console.log('advertising...');
    //
    // Once we are advertising, it's time to set up our services,
    // along with our characteristics.
    //
    bleno.setServices([
        numberService,
        deviceInfoService,
    ]);
  }
});
