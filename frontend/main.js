$(document).ready(function () {

    // Text animation setup
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

    // Siri Wave Configuration
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

    // Mic button click
    $("#MicBtn").click(function () {
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.MainExecution()();
    });

    // Hotkey trigger
    document.addEventListener('keyup', function (e) {
        if (e.key === 'j' && e.metaKey) {
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.MainExecution()();
        }
    }, false);

    // Toggle mic/send buttons based on input
    $("#chatbox").keyup(function () {
        const message = $(this).val();
        ShowHideButton(message);
    });

    // Send message via button
    $("#SendBtn").click(function () {
        const message = $("#chatbox").val();
        PlayAssistant(message);
    });

    // Send message via Enter key
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            const message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

    function ShowHideButton(message) {
        if (message.length === 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    function PlayAssistant(message) {
        if (message.trim() !== "") {
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.MainExecution(message)();
            $("#chatbox").val("");
            ShowHideButton("");
        }
    }

    // Function to render chat messages with animation
    function renderChatMessages(messages) {
        const chatCanvas = document.getElementById("chat-canvas-body");
        chatCanvas.innerHTML = ""; // Clear existing messages

        messages.forEach((msg, index) => {
            const msgDiv = document.createElement("div");

            msgDiv.className =
                msg.role === 'user'
                    ? "sender_message width-size bottom-right chat-message-animate"
                    : "receiver_message width-size bottom-left chat-message-animate";

            msgDiv.style.animationDelay = `${index * 0.05}s`;
            msgDiv.innerText = msg.content;
            chatCanvas.appendChild(msgDiv);
        });

        // Scroll to latest
        chatCanvas.scrollTop = chatCanvas.scrollHeight;
    }

    // Real-time message updating using polling
    let lastChatData = [];

    function fetchAndUpdateChat() {
        eel.get_chat_log()().then(data => {
            if (JSON.stringify(data) !== JSON.stringify(lastChatData)) {
                lastChatData = data;
                renderChatMessages(data);
            }
        });
    }

    // Initial load and periodic updates every 2 seconds
    fetchAndUpdateChat();
    setInterval(fetchAndUpdateChat, 2000);
});
