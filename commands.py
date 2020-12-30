import voice_engine as ve
import config
import datetime
import os


def process_command(command):
    if "hello" in command:
        response = f"Hello {config.username}"
        ve.response(response)
    elif "what time is it" in command:
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        response = f"It's {hour}:{minute}"
        ve.response(response)
    elif "open" in command:
        app_name = command.replace("open ", "")
        open_app(app_name)


def open_app(app_name):
    if app_name in config.apps:
        ve.response(f"Opening {app_name}")
        os.startfile(config.apps[app_name])
    else:
        ve.response(f"I couldn't find {app_name} on your app list")
