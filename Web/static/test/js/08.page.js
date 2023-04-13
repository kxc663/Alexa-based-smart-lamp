function TestPage($) {
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
    },

    onSliderChangedEvent : function(inputEvent) {
      value = Number(inputEvent.target.value);
      console.log('.... slider value has changed to: ' + value);
      obj.setSliderLabel(value);
    },

    init : function() {
      $("#power").on("click", obj.togglePower);     
      $( ".slider" ).on( "change input", obj.onSliderChangedEvent);
    },
  };
  obj.init();
  return obj;
}

jQuery(TestPage);
