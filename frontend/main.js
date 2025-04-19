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

    // Settings button click handler
    $("#SettingsBtn").click(function () {
        // Open the settings panel
        new bootstrap.Offcanvas(document.getElementById('settingsPanel')).show();

        // Load settings from server when panel opens
        eel.get_env_settings()().then(settings => {
            // Populate form fields with current settings
            $("#usernameInput").val(settings.Username || "");
            $("#modelSelect").val(settings.Model || "llama3-70b-8192");
            $("#cohereApiKey").val(settings.COHERE_API_KEY || "");
            $("#groqApiKey").val(settings.GroqAPIKey || "");
            $("#huggingFaceApiKey").val(settings.HuggingFaceAPIKey || "");
            $("#pvporcupineAccessKey").val(settings.pvporcupine_ACCESS_KEY || "");
        }).catch(err => {
            console.error("Error loading settings:", err);
        });
    });

    // Toggle password visibility
    $(".key-toggle-btn").click(function () {
        const targetId = $(this).data("target");
        const input = document.getElementById(targetId);
        const icon = $(this).find("i");

        if (input.type === "password") {
            input.type = "text";
            icon.removeClass("bi-eye").addClass("bi-eye-slash");
        } else {
            input.type = "password";
            icon.removeClass("bi-eye-slash").addClass("bi-eye");
        }
    });

    // Save settings button click handler
    $("#saveSettingsBtn").click(function () {
        const settings = {
            Username: $("#usernameInput").val(),
            Model: $("#modelSelect").val(),
            COHERE_API_KEY: $("#cohereApiKey").val(),
            GroqAPIKey: $("#groqApiKey").val(),
            HuggingFaceAPIKey: $("#huggingFaceApiKey").val(),
            pvporcupine_ACCESS_KEY: $("#pvporcupineAccessKey").val()
        };

        // Save settings via eel
        eel.save_env_settings(settings)().then(response => {
            if (response.success) {
                // Show success notification
                showNotification("Settings saved successfully!", "success");
            } else {
                // Show error notification
                showNotification("Error saving settings: " + response.message, "error");
            }
        }).catch(err => {
            showNotification("Error saving settings", "error");
            console.error("Error:", err);
        });
    });

    // Simple notification function
    function showNotification(message, type) {
        // Create notification element
        const notification = document.createElement("div");
        notification.className = `notification notification-${type}`;
        notification.innerText = message;

        // Add to body
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.classList.add("show");
        }, 10);

        // Remove after delay
        setTimeout(() => {
            notification.classList.remove("show");
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }

    // Enhance dropdown styling and behavior
    const modelSelect = document.getElementById('modelSelect');
    if (modelSelect) {
        // Add focus animation class on dropdown click
        modelSelect.addEventListener('mousedown', function () {
            this.classList.add('dropdown-clicking');
            setTimeout(() => this.classList.remove('dropdown-clicking'), 300);
        });

        // Custom event listeners for dropdown
        modelSelect.addEventListener('change', function () {
            // Add a subtle highlight effect when option changes
            this.classList.add('option-changed');
            setTimeout(() => this.classList.remove('option-changed'), 500);
        });
    }

    // Apply custom styles for the dropdown animation
    const styleForDropdown = document.createElement('style');
    styleForDropdown.textContent = `
    .dropdown-clicking {
        transform: scale(0.98);
        transition: transform 0.2s ease;
    }
    
    .option-changed {
        border-color: #0ab0d1 !important;
        box-shadow: 0 0 15px rgba(10, 176, 209, 0.7) !important;
        transition: all 0.5s ease;
    }
    
    /* This helps with the dropdown styling in dark mode */
    @media (prefers-color-scheme: dark) {
        select.settings-input option {
            background-color: #191919;
        }
    }`;

    document.head.appendChild(styleForDropdown);

    // Create custom dropdown implementation
    function createCustomDropdown() {
        const select = document.getElementById('modelSelect');
        if (!select) return;

        // Create wrapper element
        const wrapper = document.createElement('div');
        wrapper.className = 'custom-select-wrapper';
        select.parentNode.insertBefore(wrapper, select);

        // Create custom select element
        const customSelect = document.createElement('div');
        customSelect.className = 'custom-select';
        wrapper.appendChild(customSelect);

        // Create display area
        const display = document.createElement('div');
        display.className = 'custom-select-display';
        display.textContent = select.options[select.selectedIndex].textContent;
        customSelect.appendChild(display);

        // Create options container
        const options = document.createElement('div');
        options.className = 'custom-options';
        customSelect.appendChild(options);

        // Add select options to custom dropdown
        Array.from(select.options).forEach((option, index) => {
            const customOption = document.createElement('div');
            customOption.className = 'custom-option';
            customOption.textContent = option.textContent;
            customOption.dataset.value = option.value;

            if (index === select.selectedIndex) {
                customOption.classList.add('selected');
            }

            customOption.addEventListener('click', () => {
                // Update selected option
                select.value = customOption.dataset.value;
                display.textContent = customOption.textContent;

                // Update selected class
                document.querySelector('.custom-option.selected')?.classList.remove('selected');
                customOption.classList.add('selected');

                // Close dropdown
                customSelect.classList.remove('active');

                // Trigger change event on the original select
                const event = new Event('change', { bubbles: true });
                select.dispatchEvent(event);
            });

            options.appendChild(customOption);
        });

        // Toggle dropdown on click
        customSelect.addEventListener('click', (e) => {
            e.stopPropagation();
            customSelect.classList.toggle('active');
        });

        // Close dropdown when clicking elsewhere
        document.addEventListener('click', () => {
            customSelect.classList.remove('active');
        });

        // Hide original select
        select.style.display = 'none';

        // Add glow effect on hover
        customSelect.addEventListener('mouseenter', () => {
            customSelect.style.boxShadow = '0 0 10px rgba(10, 176, 209, 0.5)';
            customSelect.style.borderColor = '#0ab0d1';
        });

        customSelect.addEventListener('mouseleave', () => {
            customSelect.style.boxShadow = 'none';
            customSelect.style.borderColor = '#05738a';
        });
    }

    // Initialize custom dropdown
    createCustomDropdown();

    // Update custom dropdown when settings are loaded
    function updateCustomDropdown() {
        const select = document.getElementById('modelSelect');
        const display = document.querySelector('.custom-select-display');

        if (select && display) {
            display.textContent = select.options[select.selectedIndex].textContent;

            // Update selected option indicator
            const options = document.querySelectorAll('.custom-option');
            options.forEach(option => {
                option.classList.remove('selected');
                if (option.dataset.value === select.value) {
                    option.classList.add('selected');
                }
            });
        }
    }

    // Modify your existing settings button click handler
    const originalSettingsBtnClick = $("#SettingsBtn").click;
    $("#SettingsBtn").click(function () {
        originalSettingsBtnClick.call(this);

        // After loading settings, update the custom dropdown
        eel.get_env_settings()().then(settings => {
            // Your existing code to populate form fields

            // Add this to update the custom dropdown
            setTimeout(updateCustomDropdown, 100);
        });
    });

    // Update original settings save function to work with custom dropdown
    const originalSaveSettingsBtnClick = $("#saveSettingsBtn").click;
    $("#saveSettingsBtn").click(function () {
        // Make sure the original select has the current value
        const customSelected = document.querySelector('.custom-option.selected');
        if (customSelected) {
            document.getElementById('modelSelect').value = customSelected.dataset.value;
        }

        // Call the original save function
        originalSaveSettingsBtnClick.call(this);
    });

});
