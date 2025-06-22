$(document).ready(function () {
      // Spoken Text Animation and Display
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".assistant-message").text(message);
        $('.assistant-message').textillate('start');
        
        // Note: Orb speaking animation should be controlled separately
        // by calling startSpeaking() and stopSpeaking() functions
    }

    // Display Hood with fade-down animation (Assistant disappears upward, Hood appears from top)
    eel.expose(showHood);
    function showHood() {
        // Stop any speaking animation
        if (window.stopOrbSpeaking) {
            window.stopOrbSpeaking();
        }
        
        // Use the returnToMain function from main.js
        if (window.returnToMain) {
            window.returnToMain();
        } else {
            // Fallback animation
            $("#AssistantStatus").animate({
                opacity: 0,
                marginTop: "-50px"
            }, 200, function() {
                $("#AssistantStatus").attr("hidden", true);
                $("#AssistantStatus").css("marginTop", "0px");
                
                $("#oval").attr("hidden", false);
                $("#oval").css({
                    "opacity": 0,
                    "marginTop": "-50px"
                });
                
                $("#oval").animate({
                    opacity: 1,
                    marginTop: "0px"
                }, 200);
            });
        }
    }

    // Display Assistant with fade-up animation (Hood disappears downward, Assistant appears from bottom)
    eel.expose(showAssistant);
    function showAssistant() {
        $("#oval").animate({
            opacity: 0,
            marginTop: "50px"
        }, 200, function() {
            $("#oval").attr("hidden", true);
            $("#oval").css("marginTop", "0px");
            
            $("#AssistantStatus").attr("hidden", false);
            $("#AssistantStatus").css({
                "opacity": 0,
                "marginTop": "50px"
            });
            
            $("#AssistantStatus").animate({
                opacity: 1,
                marginTop: "0px"
            }, 200);
            
            // Start listening animation
            if (window.setOrbListening) {
                window.setOrbListening();
            }
        });
    }

    // Legacy function name support
    eel.expose(showSiri);
    function showSiri() {
        showAssistant();
    }

    // Orb control functions for backend
    eel.expose(startSpeaking);
    function startSpeaking() {
        if (window.startOrbSpeaking) {
            window.startOrbSpeaking();
        }
    }

    eel.expose(stopSpeaking);
    function stopSpeaking() {
        if (window.stopOrbSpeaking) {
            window.stopOrbSpeaking();
        }
    }

    eel.expose(setThinking);
    function setThinking() {
        if (window.setOrbThinking) {
            window.setOrbThinking();
        }
    }

    eel.expose(setListening);
    function setListening() {
        if (window.setOrbListening) {
            window.setOrbListening();
        }
    }

    eel.expose(setIdle);
    function setIdle() {
        if (window.setOrbIdle) {
            window.setOrbIdle();
        }
    }

    // Notification function
    eel.expose(showNotification);
    function showNotification() {
        if (window.showOrbNotification) {
            window.showOrbNotification();
        }
    }

    // Function to update status message without affecting orb animation
    eel.expose(updateStatusMessage);
    function updateStatusMessage(message) {
        if (window.updateStatusMessage) {
            window.updateStatusMessage(message);
        } else {
            // Fallback if the function isn't available
            const messageElement = document.querySelector('.assistant-message');
            if (messageElement) {
                messageElement.textContent = message;
            }
        }
    }

});