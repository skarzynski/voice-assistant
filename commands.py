import voice_engine as ve
import config
import datetime
import os
import webbrowser
import requests


def process_command(command):
    if "hello" in command:
        response = f"Hello {config.username}"
        ve.response(response)
    elif "what time is it" in command:
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        response = f"It's {hour}:{minute}"
        ve.response(response)
    elif "search google" in command:
        ve.response("What should I search for?")
        query = ve.recognize(ve.take_command())
        webbrowser.open_new_tab(f"https://google.com/search?q={query}")
        ve.response(f"I'm searching google for {query}")
    elif "open google" in command:
        webbrowser.open_new_tab("https://google.com")
        ve.response("Opening google")
    elif "open youtube" in command:
        webbrowser.open_new_tab("https://youtube.com")
        webbrowser.open_new_tab("test")
        ve.response("Opening youtube")
    elif "open" in command:
        app_name = command.replace("open ", "")
        open_app(app_name)
    elif "change my username" in command:
        ve.response("What should I call you?")
        new_username = ve.recognize(ve.take_command())
        change_username(new_username)
        ve.response(f"Ok, I will call you {config.username}")
    elif "how is the weather in" in command:
        place = command.replace("how is the weather in ", "")
        get_response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config.weatherapi_key}&q={place}")
        weather = get_response.json()
        if get_response.status_code != "400":
            response = f"Today in your location the temperature is {weather['current']['temp_c']} degrees and it's gonna be {weather['current']['condition']['text']}"
            ve.response(response)
        elif get_response.status_code == "400":
            ve.response(weather['error']['message'])
        else:
            ve.response("Unknown error occurred")
    elif "how is the weather" in command:
        get_response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config.weatherapi_key}&q=auto:ip")
        weather = get_response.json()
        if get_response.status_code == "200":
            response = f"Today in {weather['location']['name']} the temperature is {weather['current']['temp_c']} degrees and it's gonna be {weather['current']['condition']['text']}"
            ve.response(response)
        elif get_response.status_code == "400":
            ve.response(weather['error']['message'])
        else:
            ve.response("Unknown error occurred")
    elif "play" in command:
        url = f"{config.spotify_api_url}/play"
        requests.put(url=url, headers=config.spotify_headers)
    elif "pause" in command or "stop" in command:
        url = f"{config.spotify_api_url}/pause"
        requests.put(url=url, headers=config.spotify_headers)
    elif "next" in command:
        url = f"{config.spotify_api_url}/next"
        requests.post(url=url, headers=config.spotify_headers)
    elif "previous" in command:
        url = f"{config.spotify_api_url}/previous"
        requests.post(url=url, headers=config.spotify_headers)
    elif "volume" in command:
        percent = int(command.replace("volume ", ""))
        url = f"{config.spotify_api_url}/volume?volume_percent={percent}"
        requests.put(url=url, headers=config.spotify_headers)
    elif "what is the song" in command:
        url = f"{config.spotify_api_url}/currently-playing"
        get_response = requests.get(url=url, headers=config.spotify_headers)
        song = get_response.json()
        response = f"You are listening {song['item']['name']} by {song['item']['artists'][0]['name']}"
        ve.response(response)



def open_app(app_name):
    if app_name in config.apps:
        ve.response(f"Opening {app_name}")
        os.startfile(config.apps[app_name])
    else:
        ve.response(f"I couldn't find {app_name} on your app list")


def change_username(new_username):
    config.username = new_username
    config.save_conf()
