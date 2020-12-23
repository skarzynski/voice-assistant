import os
import gtts
import speech_recognition as sr
import playsound


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something")
        return recognizer.listen(source)


def recognize(audio):
    recognizer = sr.Recognizer()
    try:
        print("Recognizing...")
        stmt = recognizer.recognize_google(audio, language='en-in')
        response(f"You said: {stmt}")
    except Exception as e:
        print(e)
        response("I was unable to recognize your voice, try again")


def response(text):
    tts = gtts.gTTS(text=text, lang='en')
    file = 'response.mp3'
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)
