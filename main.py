import os
import eel
from backend.features import *
from backend.speechToText import *

eel.init('frontend')
os.system('start chrome.exe --app="http://localhost:8000/index.html"')
eel.start('index.html', mode=None, host='localhost', block=True)
