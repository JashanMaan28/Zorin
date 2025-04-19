$(document).ready(function () {
    
    // Spoken Text Animation and Display
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // Display Hood with fade-down animation (Siri disappears upward, Hood appears from top)
    eel.expose(showHood);
    function showHood() {
        // First animate SiriWave up and fade out
        $("#SiriWave").animate({
            opacity: 0,
            marginTop: "-50px" // Move upward while fading out
        }, 800, function() {
            // After animation completes, hide it
            $("#SiriWave").attr("hidden", true);
            // Reset position for next time
            $("#SiriWave").css("marginTop", "0px");
            
            // Prepare oval/hood to slide down from above
            $("#oval").attr("hidden", false);
            $("#oval").css({
                "opacity": 0,
                "marginTop": "-50px" // Start above its final position
            });
            
            // Animate hood coming down
            $("#oval").animate({
                opacity: 1,
                marginTop: "0px"
            }, 800);
        });
    }

    // Display Siri with fade-up animation (Hood disappears downward, Siri appears from bottom)
    eel.expose(showSiri);
    function showSiri() {
        // First animate oval/hood down and fade out
        $("#oval").animate({
            opacity: 0,
            marginTop: "50px" // Move downward while fading out
        }, 800, function() {
            // After animation completes, hide it
            $("#oval").attr("hidden", true);
            // Reset position for next time
            $("#oval").css("marginTop", "0px");
            
            // Prepare SiriWave to slide up from below
            $("#SiriWave").attr("hidden", false);
            $("#SiriWave").css({
                "opacity": 0,
                "marginTop": "50px" // Start below its final position
            });
            
            // Animate SiriWave coming up
            $("#SiriWave").animate({
                opacity: 1,
                marginTop: "0px"
            }, 800);
        });
    }

});