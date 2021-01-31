from tkinter import *
from tkinter.font import *
import tracker
import time


class popupInfo:
    def __init__(self, summonersWindow, champion, spell):
        showNotificiation(summonersWindow, champion, spell)


def showNotificiation(summonersWindow, champion, spell):
    tracker.lastCounter += 2
    counter = tracker.lastCounter
    toast = Toplevel(summonersWindow, bg="black")
    toast.attributes("-transparentcolor", toast['bg'])
    font = Font(size=17, weight='bold')
    toast.geometry('550x250+300+0')
    toast.overrideredirect(True)
    newMessage = Label(toast, text=champion.name + " has got now " + spell, font=font, fg="white", bg="black")
    newMessage.place(relx=0.5, y=15*counter, anchor=CENTER)
    time.sleep(1.5)
    for i in range(15*counter-1, 0, -1):
        newMessage.place(relx=0.5, y=i, anchor=CENTER)
        time.sleep(0.001)
    newMessage.master.destroy()
    if counter == tracker.lastCounter:
        tracker.lastCounter = -1
