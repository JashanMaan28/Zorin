import os
import eel

# Import MainExecution but don't run it automatically
from backend.commands import MainExecution

# Initialize eel
eel.init('frontend')

# Start the Chrome browser with the web app
os.system('start chrome.exe --app="http://localhost:8000/index.html"')

# Start eel web server
eel.start('index.html', mode=None, host='localhost', block=True)