$(document).ready(function () {
    
    // Spoken Text Animation and Display
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // Display Hood
    eel.expose(showHood)
    function showHood() {
        $("#oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

});