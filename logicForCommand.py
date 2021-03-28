from numba import jit
import commands
import random
import lol
import random
import os
import module.db.db_query as db

love = commands.love
commands = commands.commands

def getChamp():
    champ = random.choice(lol.champ)
    return champ["id"], champ["icon"]

def getBalancedTeam():
    team = {'champsList': []}
    needInTeam = ['Support','Marksman','Tank']    
    while True:
        champ = random.choice(lol.champ)
        champName = champ['id']
        for tag in champ['tags']:
            if tag in needInTeam or len(needInTeam) == 0:
                if tag not in team and champName not in team['champsList']:
                    if len(needInTeam) > 0:
                        needInTeam.remove(tag)
                    team[tag] = champ['icon'] 
                    team['champsList'].append(champName)
                    if len(team['champsList']) == 5:
                        return team
                        
def getMemFromDisk(pathToPhotoMemes, user, content_type):
    return __getNotSendedMeme(user, content_type, __getPhotoList(pathToPhotoMemes))

def getHelpMessage():
    helpText = ''    
    for key in commands:
        command = commands.get(key)
        helpText = helpText + command['command'] + f' --> ' + command['description'] + '\n'
    return helpText

def getVideo(user, content_type):
    return __getNotSendedMeme(user, content_type, db.getVideo())

def rank(pathToPhotoMemes, user):
    numberOfMeme = len(__getPhotoList(pathToPhotoMemes))
    seenMemes = db.getViewedMemeForUser(user.id)
    progres = format((seenMemes/numberOfMeme)*100, '.2f')
    return 'Widziałeś już {0}% memów spośród {1}'.format(progres, numberOfMeme)

def sign(user):
    db.sign(user.id, user.first_name, user.last_name, user.username)

def updateUser(user):
    db.updateUser(user.id, user.first_name, user.last_name, user.username)

def __getNotSendedMeme(user, content_type, memeList):
    historyList = db.getMemeHistoryForUser(user.id)
    notSeenMemes = (list(set(memeList) - set(historyList)))
    if len(notSeenMemes) > 0:
        meme = random.choice(notSeenMemes)
        db.updateHistory(user.id, meme, content_type)
        return meme
    return "Sory but i have sad news for you, I don't have new memes for you."

def __getPhotoList(pathToPhotoMemes):
    return os.listdir(pathToPhotoMemes)

def getLove():
    loveMeter = random.randint(1, 100)
    if loveMeter >= 90:
        return str(loveMeter) + '% ' + love[90]
    elif loveMeter >= 80:
        return str(loveMeter) + '% ' + love[80]       
    elif loveMeter >= 70:
        return str(loveMeter) + '% ' + love[70]
    elif loveMeter >= 60:
        return str(loveMeter) + '% ' + love[60]
    elif loveMeter >= 50:
        return str(loveMeter) + '% ' + love[50]
    elif loveMeter >= 40:
        return str(loveMeter) + '% ' + love[40]
    elif loveMeter >= 30:
        return str(loveMeter) + '% ' + love[30]
    elif loveMeter >= 20:
        return str(loveMeter) + '% ' + love[20]
    elif loveMeter >= 10:
        return str(loveMeter) + '% ' + love[10]
    elif loveMeter < 10:
        return str(loveMeter) + '% ' + love[5]
