import configparser
import os
import langs

cfg_file_name = "config.ini"

username = "user"
lang = langs.en
apps = dict()
weatherapi_key = "5e8d4bc583894415b4f111323203012"
# spotify_device_id = "b94fedc7a7cbd561ea2fdef64d3e8a6de508f171"
spotify_token = "BQCOhCJNvPASCNY8TiWAeJ9xnP79km7jhQNh9u8zLznRYzjVonYKNzT7IqjwhI0ZSKvMjI479gApjGfE4ENjOh4YTNuErhcwfzgl8xMO_2Hmb5qkLBXRw1q2Sz_brrUMd5_ecjC0m3xB-hSQuiuvbnz1dg "
spotify_api_url = "https://api.spotify.com/v1/me/player"
spotify_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {spotify_token}"
}


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
