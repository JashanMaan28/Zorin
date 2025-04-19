import multiprocessing
import pyautogui as autogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

# Constants
InputLanguage = "en-US"

# HTML for Speech Recognition
html_code = f'''<!DOCTYPE html>
<html lang="en">
<head><title>Speech Recognition</title></head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {{
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent = transcript;
            }};

            recognition.onend = function() {{
                recognition.start();
            }};

            recognition.start();
        }}

        function stopRecognition() {{
            recognition.stop();
            output.innerHTML = "";
        }}
    </script>
</body>
</html>'''

# Save HTML
os.makedirs("Data", exist_ok=True)
html_path = os.path.join(os.getcwd(), "Data", "Voice.html")
with open(html_path, "w") as f:
    f.write(html_code)

# Process 1: AI Runner
def startAI():
    print("Process 1 (AI) is running.")
    from main import start
    start()

# Process 2: Hotword Listener
def listenForHotword():
    print("Process 2 (Hotword listener) starting...")

    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--log-level=3")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("file:///" + html_path)
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            output_text = driver.find_element(By.ID, "output").text.lower()
            if "jarvis" in output_text:
                print("Hotword 'oracle' detected.")
                driver.find_element(By.ID, "end").click()
                autogui.hotkey("win", "j")
                print("Hotkey triggered.")
                time.sleep(1)  # Debounce
                driver.find_element(By.ID, "start").click()
        except Exception as e:
            print(f"[Hotword Error] {e}")
            time.sleep(1)

# Main launcher
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startAI)
    p2 = multiprocessing.Process(target=listenForHotword)

    p1.start()
    p2.start()

    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stopped.")
