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
        // loop: true,
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

    eel.get_chat_log()().then(data => {
        console.log("Chat log:", data);
        renderChatMessages(data);
    });    

    // Load and render messages from ChatLog.json
    fetch('ChatLog.json')
    .then(response => {
        if (!response.ok) {
            throw new Error("Could not load chat log.");
        }
        return response.json();
    })
    .then(messages => {
        renderChatMessages(messages);
    })
    .catch(error => {
        console.error("Error loading chat log:", error);
    });

    // Function to render messages into chat container
    function renderChatMessages(messages) {
        const chatCanvas = document.getElementById("chat-canvas-body");
    
        messages.forEach((msg, index) => {
            const msgDiv = document.createElement("div");
            const role = msg.role;
    
            // Assign class for role and position
            if (role === 'user') {
                msgDiv.className = "sender_message width-size bottom-right chat-message-animate";
            } else if (role === 'assistant') {
                msgDiv.className = "receiver_message width-size bottom-left chat-message-animate";
            }
    
            // Add a slight delay if you want a staggered feel
            msgDiv.style.animationDelay = `${index * 0.1}s`;
    
            msgDiv.innerText = msg.content;
            chatCanvas.appendChild(msgDiv);
        });
    }
    

});
