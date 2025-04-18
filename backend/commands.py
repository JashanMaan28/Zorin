from backend.Model import FirstLayerDMM
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from backend.features import Automation, QueryModifier
from backend.speechToText import takeCommand
from backend.ChatBot import ChatBot
from backend.textToSpeech import speak
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import eel

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = "Zorin"
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I help you?'''
subprocess = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

@eel.expose
def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    eel.DisplayMessage("Listening...")
    Query = takeCommand()
    eel.DisplayMessage(Query)
    Decision = FirstLayerDMM(Query)

    print("")
    print(f"Decision : {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Mearged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
    
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
                eel.showHood()
    
    if ImageExecution == True:

        with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery}, True")

        try:

            p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE, shell=False)
            subprocess.append(p1)
        
        except Exception as e:
            print(f"Error Starting ImageGeneration.py: {e}")
    
    if G and R or R:

        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        eel.DisplayMessage(Answer)
        speak(Answer)
        eel.showHood()
        return True
    
    else:
        for Queries in Decision:

            if "general" in Queries:
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                eel.DisplayMessage(Answer)
                speak(Answer)
                eel.showHood()
                return True
            
            elif "realtime" in Queries:
                QueryFinal = Queries.replace("realtime", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                eel.DisplayMessage(Answer)
                speak(Answer)
                eel.showHood()
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                eel.DisplayMessage(Answer)
                speak(Answer)
                eel.showHood()
                os._exit(1)
