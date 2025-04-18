from groq import Groq
from json import dump, load
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
GroqAPIKey = env_vars.get("GroqAPIKey")
Model = env_vars.get("Model")
client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named Zorin, which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in another language, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** You were made by Jashanpreet Singh, his nickname is Jashan. ***
"""

SystemChatBot = [
    {
        "role": "system",
        "content": System
    }
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Hour: {hour}\nMinute: {minute}\nSecond: {second}\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """ This function sends the user's query to the Groq API and returns the response. """

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

            messages.append(
                {
                    "role": "user",
                    "content": f"{Query}"
                }
            )

            completion = client.chat.completions.create(
                model=Model,
                messages=SystemChatBot + [{
                    "role": "user",
                    "content": RealTimeInformation()
                }] + messages,
                max_tokens=1024,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )

            Answer = ""

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")

            messages.append(
                {
                    "role": "assistant",
                    "content": Answer
                }
            )

            with open(r"Data\ChatLog.json", "w") as f:
                dump(messages, f, indent=4)

            return AnswerModifier(Answer=Answer)
        
    except Exception as e:
        print(f"An error occurred: {e}")

        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)

        return "An error occurred while processing your query. Please try again later."
