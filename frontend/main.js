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
        eel.MainExecution()();
    });


    // Hot key press Assistant Activation Event
    function doc_keyUP(e) {

        if (e.key === 'j' && e.metaKey) {
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.MainExecution()();
        }
    }
    document.addEventListener('keyup', doc_keyUP, false);

    // to PlayAssistant on typing a message
    function PlayAssistant(message) {

        if (message != "") {
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.MainExecution(message)();
            $("#chatbox").val("")
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        }
    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
    

    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

});
