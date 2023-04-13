function TestPage($) {
  var powerBtn = 'power';
  var powerState = 'powerState';
  var isPowered = false;

  obj = {
    setPowerLabel : function(label) {
      $("#powerState").html(label);
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
    },

    init : function() {
      $("#power").on("click", obj.togglePower);
    },
  };
  obj.init();
  return obj;
}

jQuery(TestPage);
