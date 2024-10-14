from os.path import exists
from time import strftime

import openai
import  speech_recognition as sr
import os
import webbrowser
from openai import OpenAI, api_key
from wikipedia import random
import random

from config import  api_key
import datetime
client = OpenAI(api_key=api_key)

chatstr = ''

def say(text):
    os.system(f"say {text}")


def open_website(query):
    website_name = query.lower().replace("open ", "").strip()
    url = f"https://www.{website_name}.com"
    webbrowser.open(url)
    say(f"Opening {website_name} for you, Sir...")

def chat(query):
    global chatstr
    openai.api_key = api_key
    chatstr += f"Abdullah: {query}\n Jarvis: "
    print(f"Chat History: {chatstr}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": chatstr
            }
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        # print("Full response ========>:", response)
        response_content = f"{response.choices[0].message.content}\n"
        chatstr += f"{response_content}\n"
        print(f"Response printing ========>: {response_content}")

        say(response_content)

        # print(f"Printing ChatStr ========>: {chatstr}")
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        filename = f"Openai/prompt_{random.randint(1, 12747842792)}.txt"
        # filename = f"Openai/{''.join(prompt.split('gpt')[1:])}.txt"
        with open(filename, "w") as f:  # "w" for writing mode
            f.write(chatstr)

        return response_content

    except Exception as e:
        print(f"Error Occured as ======> {e}")

def ai(prompt):
    text = f"OpenAi response for Prompt: {prompt} \n ****************\n\n"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        print("Full response ========>:", response)
        response_content = response.choices[0].message.content
        print("Response printing ========>:", response_content)
        text += response_content
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        filename = f"Openai/prompt_{random.randint(1, 12747842792)}.txt"
        # filename = f"Openai/{''.join(prompt.split('gpt')[1:])}.txt"
        with open(filename, "w") as f:  # "w" for writing mode
            f.write(text)
    except Exception as e:
        print(f"Error Occured as ======> {e}")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language= "en-in")
            print(f"User said: {query}")
            return  query
        except Exception as e:
            return f"Some Error Occured, Sorry."


if __name__ == '__main__':
    print("pycharm")
    say("Hello i am Jarvis A.I")
    # sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
    #          ["google", "https://www.google.com"]]
    songs = [
        ["night vibes", "/Users/abyte25/Songs/night-vibes-248407.mp3"],
        ["nighfall", "/Users/abyte25/Songs/nightfall-future-bass-music-228100.mp3"],
        ["originals", "/Users/abyte25/Songs/original-song-239607.mp3"],
        ["me", "/Users/abyte25/Songs/romantic-song-tera-roothna-by-ashir-hindi-top-trending-viral-song-231771.mp3"]
    ]
    while True:
        print("Listening... ")
        query = take_command()
        # say(query)
        print(query)
        if query:
            # for site in sites:
            #     if f"Open {site[0]}".lower() in query.lower():
            #         say(f"Opening {site[0]} Sir.....")
            #         webbrowser.open(site[1])
            #         break
            if "Open".lower() in query.lower():
                open_website(query)

            for song_name in songs:
                if f"play {song_name[0]}".lower() in query.lower():
                    say(f"playing {song_name[0]} sir....")
                    os.system(f"open {song_name[1]}")
                    break

            if "the time".lower() in query.lower():
                strftime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir the time is {strftime}")

            elif "Open Facetime".lower() in query.lower():
                os.system(f"open /System/Applications/FaceTime.app")

            elif "Open GPT".lower() in query.lower():
                ai(prompt=query)

            elif "Jarvis Quit".lower() in query.lower() or "Stop".lower() in query.lower():
                exit()

            elif "Reset Chat".lower() in query.lower():
                chatstr = ""

            else:
                print("Chatting: ")
                chat(query)
        else:
            say("Sorry, I couldn't understand that.")

