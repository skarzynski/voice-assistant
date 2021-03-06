import os
import gtts
import speech_recognition as sr
import playsound
from config import lang


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(lang["say_something"])
        return recognizer.listen(source)


def recognize(audio):
    recognizer = sr.Recognizer()
    try:
        print(f"{lang['recognizing']}...")
        stmt = recognizer.recognize_google(audio, language="en-in")
        # response(f"You said: {stmt}")
        return stmt
    except Exception as e:
        print(e)
        response(lang["unable_to_recognize"])
        return None


def response(text):
    tts = gtts.gTTS(text=text, lang="en")
    file = 'response.mp3'
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)
