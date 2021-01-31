import io
from tkinter import *
from tkinter.font import *
from roleidentification import pull_data
from roleidentification.utilities import get_team_roles
import cassiopeia
import requests
from PIL import Image, ImageTk
import threading
import time
from functools import partial
from listener import *
import popupinfo


class Tracker:
    def __init__(self, enemyTeam, summoner, nicknameWindow):
        global team, exit, nickWindow, summ, lastCounter
        lastCounter = -1
        exit = False
        summ = summoner
        nickWindow = nicknameWindow
        team = enemyTeam
        noweOkno()
        enemyTeamList()
        enemySummonerList()
        nickWindow.withdraw()
        Listening(nickWindow, summonersWindow, summoner)


def noweOkno():
    global canvaTop, canvaBot, summonersWindow
    summonersWindow = Toplevel(nickWindow)
    summonersWindow.withdraw()
    popupinfo.popupInfo(summonersWindow)
    screen_height = summonersWindow.winfo_screenheight()
    summonersWindow.geometry("360x128+200+" + str(int(screen_height - 128)))
    summonersWindow.attributes("-topmost", True)
    summonersWindow.overrideredirect(True)
    canvaTop = Canvas(summonersWindow, width=360, height=72, bd=0, highlightthickness=0)
    canvaTop.grid(row=0, column=0)
    canvaBot = Canvas(summonersWindow, bg="black", width=360, height=56, bd=0, highlightthickness=0)
    canvaBot.grid(row=1, column=0)


def enemyTeamList():
    global championList, roles
    championList = []
    champion_roles = pull_data()
    roles = get_team_roles(team, champion_roles)
    for role, champion in roles.items():
        championList.append(champion)

    raw_data = []
    nickWindow.image = []
    for champion in championList:
        raw_data.append(requests.get(cassiopeia.get_champion(champion.name).image.url))

    for i in range(len(raw_data)):
        im = Image.open(io.BytesIO(raw_data[i].content))
        im = im.resize((72, 72), Image.ANTIALIAS)
        nickWindow.image.append(ImageTk.PhotoImage(im))
        canvaTop.create_image((72 * i + 36), 36, image=nickWindow.image[i])


def summonerCounter(button, cooldown, x, y, champion, spell):
    buttonFont = Font(family='Helvetice', size=12, weight='bold')
    button['state'] = 'disabled'
    cd = Label(canvaBot, text=str(cooldown[0]), fg="white", bg="black", font=buttonFont)
    cd.place(x=x, y=y)
    timer = threading.Thread(target=timerCounter, args=(button, cd, cooldown[0], champion, spell))
    timer.start()


def infoOnTop(champion, spell):
    popupinfo.showNotificiation(champion, spell)


def timerCounter(button, label, cooldown, champion, spell):
    if cooldown == 0:
        cooldown = 300
    for i in range(cooldown, -1, -1):
        if exit:
            break
        label['text'] = i
        time.sleep(1)
    button['state'] = 'normal'
    label['text'] = ''
    t = threading.Thread(target=infoOnTop, args=(champion, spell))
    t.start()


def enemySummonerList():
    nickWindow.summImage = []
    newParticipantsList = []
    for i in range(len(championList)):
        for j in range(len(team.participants)):
            if championList[i].name == team.participants[j].champion.name:
                newParticipantsList.append(team.participants[j])
                break
    j = 0
    for i in range(len(newParticipantsList)):
        image = requests.get(newParticipantsList[i].summoner_spell_d.image.url)
        im = Image.open(io.BytesIO(image.content))
        im = im.resize((36, 36), Image.ANTIALIAS)
        nickWindow.summImage.append(ImageTk.PhotoImage(im))
        buttonD = Button(canvaBot,
                         text=newParticipantsList[i].summoner_spell_d.name,
                         image=nickWindow.summImage[j],
                         borderwidth=0,
                         fg="black",
                         bg="black",
                         activebackground="black")
        buttonD['command'] = partial(summonerCounter,
                                     buttonD,
                                     newParticipantsList[i].summoner_spell_d.cooldowns,
                                     j*36,
                                     36,
                                     newParticipantsList[i].champion,
                                     newParticipantsList[i].summoner_spell_d.name)
        buttonD.place(x=j * 36, y=0)
        j += 1
        image = requests.get(newParticipantsList[i].summoner_spell_f.image.url)
        im = Image.open(io.BytesIO(image.content))
        im = im.resize((36, 36), Image.ANTIALIAS)
        nickWindow.summImage.append(ImageTk.PhotoImage(im))
        buttonF = Button(canvaBot,
                         text=newParticipantsList[i].summoner_spell_f.name,
                         image=nickWindow.summImage[j],
                         borderwidth=0,
                         fg="black",
                         bg="black",
                         activebackground="black")
        buttonF['command'] = partial(summonerCounter,
                                     buttonF,
                                     newParticipantsList[i].summoner_spell_f.cooldowns,
                                     j*36,
                                     36,
                                     newParticipantsList[i].champion,
                                     newParticipantsList[i].summoner_spell_f.name)
        buttonF.place(x=j * 36, y=0)
        j += 1
