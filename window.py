from tkinter import *
from tkinter import ttk
from tkinter.font import *
import cassiopeia
from tracker import *
import os
import configparser


class Window:
    def __init__(self):
        global nicknameWindow
        nicknameWindow = Tk()
        init()
        labelAboutPlayer()
        inputField()
        lastUsedSummoners()
        buttons()
        deleteUserButton()
        serverList()
        nicknameWindow.mainloop()


def getlist(value):
    return value.split(os.linesep)


def lastUsedSummoners():
    global config, lastSummonersList, configPath, temp
    temp = []
    lastSummonersList = []
    config = configparser.ConfigParser(converters={"list": getlist})
    dir_path = '%s\\Summoners Tracker\\' % os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    configPath = dir_path + 'settings.ini'

    if not os.path.exists(configPath):
        config.write(open(configPath, 'w'))
    else:
        config.read(configPath)

    if config.has_section('NICKNAMES'):
        temp = config.items("NICKNAMES")
    else:
        config.add_section('NICKNAMES')

    for i in range(len(temp)):
        lastSummonersList.append(str(temp[i][0]))

    inputNick['values'] = lastSummonersList


def init():
    nicknameWindow.title("LoL Summoners Tracker")
    screen_height = nicknameWindow.winfo_screenheight()
    screen_width = nicknameWindow.winfo_screenwidth()
    position = str(int(screen_width / 2) - 150) + '+' + str(int(screen_height / 2) - 200)
    nicknameWindow.geometry('300x400+' + position)
    nicknameWindow.resizable(False, False)


def updateSelectedRegion(event):
    index = inputNick.current()
    serverIndex = SERVERS.index(temp[index][1])
    serversList.current(serverIndex)


def inputField():
    global inputNick
    labelNick = Label(nicknameWindow, text="Nickname", font=('Arial', 15), justify=CENTER)
    labelNick.place(relx=0.5, y=60, anchor=CENTER)
    inputNick = ttk.Combobox(nicknameWindow, font=('Arial', 18), width=15, justify='center')
    inputNick.place(relx=0.5, y=100, anchor=CENTER)
    inputNick.bind("<<ComboboxSelected>>", updateSelectedRegion)


def deleteUser():
    if inputNick.get() != "":
        if inputNick.get() in lastSummonersList:
            selectedUserIndex = inputNick.current()
            config.remove_option('NICKNAMES', temp[selectedUserIndex][0])
            del temp[selectedUserIndex]
            del lastSummonersList[selectedUserIndex]
            with open(configPath, 'w') as configfile:
                config.write(configfile)
            inputNick['values'] = lastSummonersList
            inputNick.set('')


def deleteUserButton():
    deleteUserB = Button(nicknameWindow, text="Delete selected user", font=('Arial', 12), command=deleteUser, fg="red")
    deleteUserB.place(relx=0.5, y=155, anchor=CENTER)


def buttons():
    nextB = Button(nicknameWindow, text="Confirm", font=('Arial', 14),
                   command=buttonClick)
    nextB.place(relx=0.5, y=300, anchor=CENTER)


def labelAboutPlayer():
    global infoLabel
    font = Font(family='Helvetica', size=12, weight="bold")
    infoLabel = Label(nicknameWindow, text="", font=font, fg="red", anchor='center')
    infoLabel.pack()


def addSummonerToList(summoner):
    if summoner.name not in lastSummonersList:
        config.set('NICKNAMES', summoner.name, serversList.get())
    with open(configPath, 'w') as configfile:
        config.write(configfile)
    lastUsedSummoners()


def showSummoners(summoner):
    infoLabel['text'] = ""
    try:
        if summoner.current_match.exists:

            addSummonerToList(summoner)

            teams = summoner.current_match

            if summoner in teams.blue_team.participants:
                Tracker(teams.red_team, summoner, nicknameWindow)
            else:
                Tracker(teams.blue_team, summoner, nicknameWindow)
            infoLabel['text'] = ""
    except:
        infoLabel['text'] = summoner.name + " is not in game!"


def buttonClick():
    if inputNick.get() != "":
        summoner = cassiopeia.get_summoner(name=inputNick.get(), region=serversList.get())
        if summoner.exists:
            cassiopeia.set_default_region(serversList.get())
            t = threading.Thread(target=showSummoners, args=[summoner])
            t.start()


def serverList():
    global SERVERS
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

    global serversList

    font = Font(family='Helvetica', size=14)
    serversList = ttk.Combobox(nicknameWindow, width=10, font=font, values=SERVERS, justify=CENTER)
    serversList.place(relx=0.5, y=210, anchor=CENTER)
    serversList.current(0)
