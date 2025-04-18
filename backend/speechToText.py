############################################################
#          Speech Recognition Module {TYPE - 1} (Best)
############################################################


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import mtranslate as mt
import eel

InputLanguage = "en-US"

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()

Link = f"{current_dir}/Data/Voice.html"

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.3"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")  # Run in headless mode for automation

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

TempDirPath = rf"{current_dir}/Frontend/Files"


def QueryModifier(Query):
    new_query = Query.lower().strip()
    question_words = [
        "what", "who", "where", "when", "why", "how", "which", "whose", "whom",
        "can you", "how's", "where's", "what's"
    ]

    is_question = any(new_query.startswith(word) for word in question_words)

    if is_question:
        if not new_query.endswith("?"):
            new_query += "?"
    else:
        if not new_query.endswith((".", "!", "?")):
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def takeCommand():
    print("Listening...")
    driver.get("file:///" + Link)
    driver.find_element(By.ID, value="start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, value="output").text

            if Text:
                driver.find_element(By.ID, value="end").click()
                
                print("Recognizing...")
                
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    result = QueryModifier(Text)
                else:
                    print("Translating...")
                    result = QueryModifier(UniversalTranslator(Text))
                
                print(f"User said: {result}\n")
                
                return result
        except Exception as e:
            pass



############################################################
#          Speech Recognition Module {TYPE - 2} (Not Recommended)
############################################################


# import speech_recognition as sr
# from backend.textToSpeech import speak
# import eel

# @eel.expose # Expose the function to JavaScript
# def takeCommand():
#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         print("Listening...")
#         eel.DisplayMessage("Listening...")  # Display message in the frontend
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)

#         audio = r.listen(source, 10, 6)

#     try:
#         print("Recognizing...")
#         eel.DisplayMessage("Recognizing...")  # Display message in the frontend
#         query = r.recognize_google(audio, language='en-US')
#         print(f"User said: {query}\n")
#         eel.DisplayMessage(query)
#         speak(query)  # Speak the recognized text
#         eel.showHood()
#     except Exception as e:
#         return ""
    
#     return query.lower()

