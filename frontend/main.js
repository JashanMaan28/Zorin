$(document).ready(function () {
    
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: 'bounceIn',
        },
        out: {
            effect: 'bounceOut',
        }
    });

    // Siri Configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 900,
        height: 200,
        style: "ios9",
        amplitude: "2",
        speed: "0.05",
        autostart: true
      });

    // Siri Message Animation
      $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: 'fadeInUp',
            sync: true,
        },
        out: {
            effect: 'fadeOutUp',
            sync: true,
        }
    });
    
    // Mic Button Click Event
    $("#MicBtn").click(function () {
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        
    });

});