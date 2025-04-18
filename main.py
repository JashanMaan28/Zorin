import os
import eel

# Import MainExecution but don't run it automatically
from backend.commands import MainExecution

def start():
    eel.init('frontend')
    os.system('start chrome.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)
