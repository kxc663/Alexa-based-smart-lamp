function TestPage($) {
  var powerBtn = 'power';
  var powerState = 'powerState';
  var isPowered = false;
  var slider = 'slider';
  var sliderState = 'sliderState';


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

    setSliderLabel : function(label) {
      $("#sliderState").html(label);
    },

    onSliderChangedEvent : function() {
      var slide = $("#slider");
      console.log('.... slider value has changed to: ' + slide.val());
      obj.setSliderLabel(slide.val());
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
