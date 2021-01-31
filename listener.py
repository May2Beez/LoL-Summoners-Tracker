from pynput import *
from pynput.keyboard import *
import tracker as track
import time
import popupinfo as ppi


class Listening:
    def __init__(self, nicknameWindow, summonersWindow, summoner):
        global nickWindow, summWindow, summ, h, listener
        nickWindow = nicknameWindow
        summWindow = summonersWindow
        summ = summoner
        h = GlobalHotKeys({'<alt>+e': exitProgram})
        h.start()
        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()


def exitProgram():
    track.exit = True
    time.sleep(1.1)
    summWindow.destroy()
    nickWindow.deiconify()
    ppi.toast.destroy()
    h.stop()
    listener.stop()


def on_press(key):
    if key == Key.tab:
        summWindow.deiconify()


def on_release(key):
    if key == Key.tab:
        summWindow.withdraw()