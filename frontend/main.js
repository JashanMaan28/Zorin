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
    });    // AI Orb Animation Controller
    class OrbController {
        constructor() {
            this.mainOrb = document.getElementById('aiOrb');
            this.statusOrb = document.getElementById('statusOrb');
            this.currentState = 'idle';
            this.isAnimating = false;
        }

        // Set orb state: 'idle', 'listening', 'thinking', 'speaking'
        setState(state, orbElement = null) {
            const orb = orbElement || this.mainOrb;
            if (!orb) return;

            // Prevent conflicting state changes
            if (this.isAnimating && state === this.currentState) return;

            this.isAnimating = true;

            // Remove all animation classes
            orb.classList.remove('orb-listening', 'orb-thinking', 'orb-speaking');
            
            // Add new state class
            switch(state) {
                case 'listening':
                    orb.classList.add('orb-listening');
                    break;
                case 'thinking':
                    orb.classList.add('orb-thinking');
                    break;
                case 'speaking':
                    orb.classList.add('orb-speaking');
                    break;
                case 'idle':
                default:
                    // Default idle animation is handled by CSS
                    break;
            }
            
            this.currentState = state;
            
            // Reset animation flag after transition
            setTimeout(() => {
                this.isAnimating = false;
            }, 300);
        }

        // Start speaking animation
        startSpeaking(orbElement = null) {
            this.setState('speaking', orbElement);
        }

        // Stop speaking animation - returns to idle, not listening
        stopSpeaking(orbElement = null) {
            this.setState('idle', orbElement);
        }

        // Start listening animation
        startListening(orbElement = null) {
            this.setState('listening', orbElement);
        }

        // Start thinking animation
        startThinking(orbElement = null) {
            this.setState('thinking', orbElement);
        }

        // Return to idle state
        setIdle(orbElement = null) {
            this.setState('idle', orbElement);
        }

        // Get current state
        getCurrentState() {
            return this.currentState;
        }
    }

    // Initialize orb controller
    const orbController = new OrbController();

    // Assistant message animation
    $('.assistant-message').textillate({
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

    // Animated transition to show assistant interface
    function animateToAssistant() {
        // First animate oval/hood down and fade out
        $("#oval").animate({
            opacity: 0,
            marginTop: "50px" // Move downward while fading out
        }, 800, function() {
            // After animation completes, hide it
            $("#oval").attr("hidden", true);
            // Reset position for next time
            $("#oval").css("marginTop", "0px");
            
            // Prepare Assistant Status to slide up from below
            $("#AssistantStatus").attr("hidden", false);
            $("#AssistantStatus").css({
                "opacity": 0,
                "marginTop": "50px" // Start below its final position
            });
            
            // Animate Assistant Status coming up
            $("#AssistantStatus").animate({
                opacity: 1,
                marginTop: "0px"
            }, 800);

            // Start listening animation on status orb
            orbController.startListening(document.getElementById('statusOrb'));
        });
    }    // Mic button click with animation
    $("#MicBtn").click(function () {
        animateToAssistant();
        // Add slight delay before triggering MainExecution to allow animation to begin
        setTimeout(function() {
            eel.MainExecution()();
        }, 300);
    });

    // Hotkey trigger with animation
    document.addEventListener('keyup', function (e) {
        if (e.key === 'j' && e.metaKey) {
            animateToAssistant();
            // Add slight delay before triggering MainExecution to allow animation to begin
            setTimeout(function() {
                eel.MainExecution()();
            }, 300);
        }
    }, false);

    // Toggle mic/send buttons based on input
    $("#chatbox").keyup(function () {
        const message = $(this).val();
        ShowHideButton(message);
    });    // Send message via button with animation
    $("#SendBtn").click(function () {
        const message = $("#chatbox").val();
        if (message.trim() !== "") {
            animateToAssistant();
            // Add slight delay before triggering MainExecution to allow animation to begin
            setTimeout(function() {
                eel.MainExecution(message)();
                $("#chatbox").val("");
                ShowHideButton("");
            }, 300);
        }
    });

    // Send message via Enter key with animation
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            const message = $("#chatbox").val();
            if (message.trim() !== "") {
                animateToAssistant();
                // Add slight delay before triggering MainExecution to allow animation to begin
                setTimeout(function() {
                    eel.MainExecution(message)();
                    $("#chatbox").val("");
                    ShowHideButton("");
                }, 300);
            }
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
    }    // Original PlayAssistant function is now replaced by the animateToAssistant + delayed execution pattern
    function PlayAssistant(message) {
        if (message.trim() !== "") {
            animateToAssistant();
            // Add slight delay before triggering MainExecution
            setTimeout(function() {
                eel.MainExecution(message)();
                $("#chatbox").val("");
                ShowHideButton("");
            }, 300);
        }
    }    // Message and state synchronization helper
    function updateAssistantMessage(message, forceUpdate = false) {
        const messageElement = document.querySelector('.assistant-message');
        if (messageElement && (forceUpdate || !messageElement.textContent.includes('...'))) {
            messageElement.textContent = message;
        }
    }

    // Enhanced orb state management with message synchronization
    window.startOrbSpeaking = function() {
        orbController.startSpeaking();
        orbController.startSpeaking(document.getElementById('statusOrb'));
        updateAssistantMessage('Speaking...', true);
    };

    window.stopOrbSpeaking = function() {
        orbController.stopSpeaking();
        orbController.stopSpeaking(document.getElementById('statusOrb'));
        // Don't automatically change message - let the backend control the next state
    };

    window.setOrbThinking = function() {
        orbController.startThinking();
        orbController.startThinking(document.getElementById('statusOrb'));
        updateAssistantMessage('Thinking...', true);
    };

    window.setOrbListening = function() {
        orbController.startListening();
        orbController.startListening(document.getElementById('statusOrb'));
        updateAssistantMessage('Listening...', true);
    };

    window.setOrbIdle = function() {
        orbController.setIdle();
        orbController.setIdle(document.getElementById('statusOrb'));
        updateAssistantMessage('Ready...', true);
    };

    // Function to update message without changing orb state
    window.updateStatusMessage = function(message) {
        updateAssistantMessage(message, true);
    };

    // Function to get current orb state
    window.getOrbState = function() {
        return orbController.getCurrentState();
    };

    // Return to main interface function
    window.returnToMain = function() {
        // Hide assistant status
        $("#AssistantStatus").animate({
            opacity: 0,
            marginTop: "50px"
        }, 600, function() {
            $("#AssistantStatus").attr("hidden", true);
            $("#AssistantStatus").css("marginTop", "0px");
            
            // Show main interface
            $("#oval").attr("hidden", false);
            $("#oval").css({
                "opacity": 0,
                "marginTop": "50px"
            });
            
            $("#oval").animate({
                opacity: 1,
                marginTop: "0px"
            }, 600);

            // Reset orb to idle
            orbController.setIdle();
        });
    };

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

    // Enhanced orb interactions
    function addOrbInteractions() {
        const mainOrb = document.getElementById('aiOrb');
        const statusOrb = document.getElementById('statusOrb');

        // Add hover effects to main orb
        if (mainOrb) {
            mainOrb.addEventListener('mouseenter', function() {
                if (orbController.currentState === 'idle') {
                    this.style.transform = 'scale(1.05)';
                    this.style.transition = 'transform 0.3s ease';
                }
            });

            mainOrb.addEventListener('mouseleave', function() {
                if (orbController.currentState === 'idle') {
                    this.style.transform = 'scale(1)';
                }
            });

            // Add click effect
            mainOrb.addEventListener('click', function() {
                // Create ripple effect
                const ripple = document.createElement('div');
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(10, 176, 209, 0.3);
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    width: 100px;
                    height: 100px;
                    left: 50%;
                    top: 50%;
                    margin-left: -50px;
                    margin-top: -50px;
                    pointer-events: none;
                `;
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        }
    }

    // Add ripple animation CSS
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        /* Smooth transitions for orb states */
        .square {
            transition: transform 0.3s ease;
        }
        
        /* Enhanced glow effect for active states */
        .orb-active {
            filter: brightness(1.2) contrast(1.1);
        }
        
        /* Pulse effect for notifications */
        .orb-notification {
            animation: orbNotification 1s ease-in-out 3;
        }
        
        @keyframes orbNotification {
            0%, 100% {
                transform: scale(1);
                box-shadow: 
                    0 0 80px rgba(10, 176, 209, 0.6),
                    inset 0 0 40px rgba(10, 176, 209, 0.3),
                    0 0 120px rgba(41, 233, 221, 0.4);
            }
            50% {
                transform: scale(1.1);
                box-shadow: 
                    0 0 150px rgba(10, 176, 209, 1),
                    inset 0 0 60px rgba(10, 176, 209, 0.5),
                    0 0 200px rgba(41, 233, 221, 0.8);
            }
        }
    `;
    document.head.appendChild(rippleStyle);

    // Initialize interactions
    addOrbInteractions();

    // Notification function for orb
    window.showOrbNotification = function() {
        const orbs = [document.getElementById('aiOrb'), document.getElementById('statusOrb')];
        orbs.forEach(orb => {
            if (orb) {
                orb.classList.add('orb-notification');
                setTimeout(() => {
                    orb.classList.remove('orb-notification');
                }, 3000);
            }
        });
    };

    // Auto-detect speaking state changes (for voice playback)
    let speechDetectionInterval;
    
    window.startSpeechDetection = function() {
        if (speechDetectionInterval) return;
        
        speechDetectionInterval = setInterval(() => {
            // Check if audio is playing (you may need to adapt this to your audio system)
            const audioElements = document.querySelectorAll('audio');
            let isPlaying = false;
            
            audioElements.forEach(audio => {
                if (!audio.paused && !audio.ended) {
                    isPlaying = true;
                }
            });
            
            if (isPlaying && orbController.currentState !== 'speaking') {
                window.startOrbSpeaking();
            } else if (!isPlaying && orbController.currentState === 'speaking') {
                window.stopOrbSpeaking();
            }
        }, 100);
    };
    
    window.stopSpeechDetection = function() {
        if (speechDetectionInterval) {
            clearInterval(speechDetectionInterval);
            speechDetectionInterval = null;
        }
    };

    // Enhanced textbox functionality
    function initializeTextboxEnhancements() {
        const chatbox = document.getElementById('chatbox');
        const textInput = document.getElementById('TextInput');
        const charCounter = document.getElementById('charCounter');
        const charCount = document.querySelector('.char-count');
        const sendBtn = document.getElementById('SendBtn');
        const micBtn = document.getElementById('MicBtn');

        if (!chatbox || !charCounter) return;

        // Character counter functionality
        function updateCharCounter() {
            const length = chatbox.value.length;
            const maxLength = parseInt(chatbox.getAttribute('maxlength')) || 500;
            
            charCount.textContent = length;
            
            // Show/hide counter based on input
            if (length > 0) {
                charCounter.classList.add('visible');
            } else {
                charCounter.classList.remove('visible');
            }
            
            // Warning states
            charCounter.classList.remove('warning', 'error');
            if (length > maxLength * 0.9) {
                charCounter.classList.add('warning');
            }
            if (length >= maxLength) {
                charCounter.classList.add('error');
            }
        }

        // Enhanced input events
        chatbox.addEventListener('input', function(e) {
            updateCharCounter();
            
            // Auto-resize behavior (if needed for future textarea upgrade)
            this.style.height = 'auto';
            
            // Trigger button visibility
            ShowHideButton(this.value);
        });

        // Focus enhancement
        chatbox.addEventListener('focus', function() {
            textInput.classList.add('focused');
        });

        chatbox.addEventListener('blur', function() {
            textInput.classList.remove('focused');
        });

        // Typing indicator simulation
        let typingTimeout;
        chatbox.addEventListener('keydown', function() {
            clearTimeout(typingTimeout);
            
            // Show typing indicator (you can integrate this with backend)
            if (window.showTypingIndicator) {
                window.showTypingIndicator();
            }
            
            typingTimeout = setTimeout(() => {
                if (window.hideTypingIndicator) {
                    window.hideTypingIndicator();
                }
            }, 1000);
        });

        // Submit on Ctrl+Enter
        chatbox.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                if (this.value.trim() !== "") {
                    sendBtn.click();
                }
            }
        });

        // Paste enhancement
        chatbox.addEventListener('paste', function(e) {
            setTimeout(() => {
                updateCharCounter();
                // Clean up pasted content if needed
                const maxLength = parseInt(this.getAttribute('maxlength')) || 500;
                if (this.value.length > maxLength) {
                    this.value = this.value.substring(0, maxLength);
                    updateCharCounter();
                }
            }, 10);
        });

        // Loading state management
        window.setTextboxLoading = function(loading) {
            if (loading) {
                textInput.classList.add('loading');
                chatbox.disabled = true;
            } else {
                textInput.classList.remove('loading');
                chatbox.disabled = false;
            }
        };

        // Success feedback
        window.showTextboxSuccess = function() {
            textInput.classList.add('success');
            setTimeout(() => {
                textInput.classList.remove('success');
            }, 600);
        };

        // Voice input state management
        window.setMicListening = function(listening) {
            if (listening) {
                micBtn.classList.add('listening');
                micBtn.querySelector('i').className = 'bi bi-mic-fill';
            } else {
                micBtn.classList.remove('listening');
                micBtn.querySelector('i').className = 'bi bi-mic';
            }
        };

        // Recording state
        window.setMicRecording = function(recording) {
            if (recording) {
                micBtn.classList.add('recording');
                micBtn.querySelector('i').className = 'bi bi-record-circle';
            } else {
                micBtn.classList.remove('recording');
                micBtn.querySelector('i').className = 'bi bi-mic';
            }
        };

        // Chat notification management
        window.setChatNotification = function(hasNew) {
            const chatBtn = document.getElementById('ChatBtn');
            if (hasNew) {
                chatBtn.classList.add('has-new-messages');
            } else {
                chatBtn.classList.remove('has-new-messages');
            }
        };

        // Typing indicator management
        window.showTypingIndicator = function() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.classList.add('active');
            }
        };

        window.hideTypingIndicator = function() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.classList.remove('active');
            }
        };

        // Clear input helper
        window.clearTextbox = function() {
            chatbox.value = '';
            updateCharCounter();
            ShowHideButton('');
            chatbox.focus();
        };

        // Set textbox value helper
        window.setTextboxValue = function(value) {
            chatbox.value = value;
            updateCharCounter();
            ShowHideButton(value);
        };

        // Focus textbox helper
        window.focusTextbox = function() {
            chatbox.focus();
        };

        // Initialize counter
        updateCharCounter();
    }

    // Initialize enhanced textbox functionality
    initializeTextboxEnhancements();

});


    /*
     * AI Orb Animation System Usage Guide
     * ==================================
     * 
     * The orb controller provides the following methods:
     * 
     * From JavaScript:
     * - orbController.setState('idle|listening|thinking|speaking')
     * - orbController.startSpeaking() / stopSpeaking()
     * - orbController.startListening()
     * - orbController.startThinking()
     * - orbController.setIdle()
     * 
     * From Python (via eel):
     * - eel.startSpeaking()()
     * - eel.stopSpeaking()()
     * - eel.setThinking()()
     * - eel.setListening()()
     * - eel.setIdle()()
     * - eel.showNotification()()
     */

    /*
     * USAGE GUIDE FOR BACKEND DEVELOPERS
     * ==================================
     * 
     * To fix the "speaking/listening" bug, use these functions in the correct sequence:
     * 
     * 1. When user starts speaking:
     *    eel.setListening()()  # Sets orb to listening state with "Listening..." message
     * 
     * 2. When processing user input:
     *    eel.setThinking()()   # Sets orb to thinking state with "Thinking..." message
     * 
     * 3. When assistant starts speaking:
     *    eel.startSpeaking()() # Sets orb to speaking state with "Speaking..." message
     * 
     * 4. When assistant finishes speaking:
     *    eel.stopSpeaking()()  # Stops speaking animation (no automatic message change)
     *    eel.setListening()()  # Explicitly set to listening state with "Listening..." message
     * 
     * 5. To display custom messages without changing orb state:
     *    eel.updateStatusMessage("Custom message")()
     * 
     * 6. To display assistant responses:
     *    eel.DisplayMessage("Assistant response")()  # Only updates text, doesn't change orb state
     * 
     * IMPORTANT: DisplayMessage() no longer automatically triggers speaking animation!
     * You must explicitly call startSpeaking() and stopSpeaking() when audio plays.
     */

    // Initialize speech detection for automatic orb animation
    // This will automatically start/stop speaking animation based on audio playback
    if (typeof window.startSpeechDetection === 'function') {
        window.startSpeechDetection();
    }

    // Performance monitoring for orb animations
    if (typeof performance !== 'undefined' && performance.mark) {
        performance.mark('orb-system-initialized');
    }