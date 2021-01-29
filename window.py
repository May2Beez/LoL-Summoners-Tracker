from tkinter import *
from tkinter.font import *
import cassiopeia
from tracker import *


class Window:
    def __init__(self):
        global nicknameWindow
        nicknameWindow = Tk()
        init()
        labelAboutPlayer()
        inputField()
        buttons()
        serverList()
        nicknameWindow.mainloop()


def init():
    nicknameWindow.title("LoL Summoners Tracker")
    screen_height = nicknameWindow.winfo_screenheight()
    screen_width = nicknameWindow.winfo_screenwidth()
    position = str(int(screen_width / 2) - 150) + '+' + str(int(screen_height / 2) - 200)
    nicknameWindow.geometry('300x400+' + position)


def inputField():
    global labelNick, inputNick
    labelNick = Label(nicknameWindow, text="Nickname", font=('Arial', 15), justify=CENTER)
    labelNick.place(relx=0.5, y=60, anchor=CENTER)
    inputNick = Entry(nicknameWindow, font=('Arial', 18), width=15, justify='center')
    inputNick.place(relx=0.5, y=100, anchor=CENTER)


def buttons():
    nextB = Button(nicknameWindow, text="Confirm", font=('Arial', 14), command=buttonClick)
    nextB.place(relx=0.5, y=300, anchor=CENTER)


def labelAboutPlayer():
    global infoLabel
    font = Font(family='Helvetica', size=12, weight="bold")
    infoLabel = Label(nicknameWindow, text="", font=font, fg="red", anchor='center')
    infoLabel.pack()


def showSummoners(summoner):
    infoLabel['text'] = ""
    try:
        if summoner.current_match.exists:
            teams = summoner.current_match

            if summoner in teams.blue_team.participants:
                pass
                Tracker(teams.red_team, summoner, nicknameWindow)
            else:
                pass
                Tracker(teams.blue_team, summoner, nicknameWindow)
            infoLabel['text'] = ""
    except:
        infoLabel['text'] = summoner.name + " is not in game!"


def buttonClick():
    if inputNick.get() != "":
        summoner = cassiopeia.get_summoner(name=inputNick.get(), region=servers.get())
        if summoner.exists:
            cassiopeia.set_default_region(servers.get())
            showSummoners(summoner)


def serverList():
    SERVERS = [
        "EUNE",
        "EUW",
        "NA",
        "KR",
        "JP",
        "BR",
        "LAN",
        "LAS",
        "OCE",
        "RU",
        "TR"
    ]

    global servers
    servers = StringVar(nicknameWindow)
    servers.set(SERVERS[0])

    font = Font(family='Helvetica', size=14)
    global list
    list = OptionMenu(nicknameWindow, servers, *SERVERS)
    list.config(font=font)
    list.place(relx=0.5, y=170, anchor=CENTER)
