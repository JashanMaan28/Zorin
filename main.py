import os
import eel
import json

# Import MainExecution but don't run it automatically
from backend.commands import MainExecution

def start():
    eel.init('frontend')
    os.system('start chrome.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)

@eel.expose
def get_chat_log():
    file_path = "Data\ChatLog.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading chat log:", e)
        return []