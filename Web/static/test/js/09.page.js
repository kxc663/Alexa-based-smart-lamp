function TestPage($) {
  var isPowered = false;
  //const hostAddress = "http://ec2-54-82-61-44.compute-1.amazonaws.com";
  const hostAddress = window.location.hostname;
  const hostPort = "50002";
  const clientId = Math.random() + "_web_client";
  const deviceId = "TEST";

  var configurationState = {};
  console.log(clientId);
  var client = new Paho.MQTT.Client(hostAddress, Number(hostPort), clientId);
  var updateTimer = null;
  var isPowered = false;

  obj = {

    setPowerLabel : function(label) {
      $("#powerState").html(label);
    },

    setSliderLabel : function(label) {
      $("#sliderState").html(label);
    },

    powerOn : function () {
      console.log('.... powering on');
      obj.setPowerLabel("On");
      isPowered = true;
    },
    powerOff : function () {
      console.log('.... powering off');
      obj.setPowerLabel("Off");
      isPowered = false;
    },

    togglePower : function() {
      console.log('.... toggling power');
      if (isPowered)
        obj.powerOff();
      else
        obj.powerOn();
      message = new Paho.MQTT.Message(JSON.stringify(isPowered));
      message.destinationName = "devices/somedevice/power";
      message.qos = 1;
      client.send(message);
      obj.sendConfigChange();
    },

    onSliderChangedEvent : function(inputEvent) {
      value = Number(inputEvent.target.value);
      console.log('.... slider value has changed to: ' + value);
      obj.setSliderLabel(value);
    },
    sendConfigChange : function() {
      configJson = JSON.stringify(configurationState);
      message = new Paho.MQTT.Message(configJson);
      message.destinationName = "devices/" + deviceId + "/test/poke_value";
      client.send(message);
    },

    scheduleConfigChange : function() {
      function onTimeout() {
        updateTimer = null;
        obj.sendConfigChange();
      }

      if(updateTimer == null) {
        updateTimer = setTimeout(onTimeout, 100);
      }
    },

    connect : function() {
      client.connect({
            onSuccess:obj.onConnect,
            onFailure:obj.onFailure,
        });
    },

    onFailure : function(response) {
      console.log(response);
    },

    onConnect : function(response) {
      client.subscribe("devices/+/label/changed");
    },

    onConnectionLost : function(responseObject) {
      if (responseObject.errorCode !== 0) {
          console.log("onConnectionLost:"+responseObject.errorMessage);
          obj.connect();
      }
    },

    onMessageArrived : function(message) {
      console.log(message);
      console.log(message.payloadString);
      configurationState = JSON.parse(message.payloadString);
      console.log(configurationState);
      obj.updateUI();
      },

    updateUI : function() {
      $("#sub_value").html(configurationState.value);
    },

    init : function() {
      client.onConnectionLost = obj.onConnectionLost;
      client.onMessageArrived = obj.onMessageArrived;
      obj.connect();

      $("#power").on("click", obj.togglePower);     
      $( ".slider" ).on( "change input", obj.onSliderChangedEvent);
    },
  };
  obj.init();
  return obj;
}

jQuery(TestPage);
