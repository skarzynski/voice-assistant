import configparser
import os

cfg_file_name = "config.ini"


def conf():
    if not os.path.isfile(cfg_file_name):
        cfg_file = open(cfg_file_name, 'w')

        cfg = configparser.ConfigParser()

        cfg.add_section('user')
        cfg.set('user', 'username', 'user')
        cfg.set('user', 'lang', 'en')

        cfg.add_section('apps')
        cfg.set('apps', 'spotify', 'C:\\ProgramFiles\\Spotify\\Spotify.exe')

        cfg.write(cfg_file)
        cfg_file.close()
