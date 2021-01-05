import config
from gui import gui

if __name__ == '__main__':
    # ve.recognize(ve.take_command())
    config.init_conf()
    config.load_conf()
    gui()
