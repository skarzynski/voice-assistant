import configparser
import os
import langs

cfg_file_name = "config.ini"

username = "user"
lang = langs.en
apps = dict()
weatherapi_key = "5e8d4bc583894415b4f111323203012"


def init_conf():
    if not os.path.isfile(cfg_file_name):
        cfg_file = open(cfg_file_name, 'w')

        cfg = configparser.ConfigParser()

        cfg.add_section('user')
        cfg.set('user', 'username', 'user')
        cfg.set('user', 'lang', 'en')

        cfg.add_section('apps')
        cfg.set('apps', 'spotify', 'C:/Users/szymo/AppData/Roaming/Spotify/Spotify.exe')

        cfg.write(cfg_file)
        cfg_file.close()


def load_conf():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    global username
    global lang

    username = cfg['user']['username']
    lang = langs.languages_short[cfg['user']['lang']]

    apps.clear()

    for app in cfg['apps']:
        apps[app] = cfg['apps'][app]


def save_conf():
    cfg = configparser.ConfigParser()

    cfg.read('config.ini')

    cfg.set('user', 'username', username)
    cfg.set('user', 'lang', lang["out_lang"])

    for app in cfg['apps']:
        cfg.remove_option('apps', app)

    for app in apps:
        cfg.set('apps', app, apps[app])

    cfg_file = open(cfg_file_name, 'w')
    cfg.write(cfg_file)
    cfg_file.close()
