import os
import gtts
import speech_recognition as sr
import playsound
import langs

lang = langs.en

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(lang["say_something"])
        return recognizer.listen(source)


def recognize(audio):
    recognizer = sr.Recognizer()
    try:
        print(f"{lang['recognizing']}...")
        stmt = recognizer.recognize_google(audio, language=lang["in_lang"])
        response(f"You said: {stmt}")
    except Exception as e:
        print(e)
        response(lang["unable_to_recognize"])


def response(text):
    tts = gtts.gTTS(text=text, lang=lang["out_lang"])
    file = 'response.mp3'
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)
