#!/usr/bin/python3

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from configparser import ConfigParser
import json
import time
import commands
import logicForCommand
import module.db.db_query as db

config = ConfigParser()
config.read('/home/termi/bot_telegram/config.ini')
pathToPhotoMemes = config.get('path', 'pathToPhotoMemes')
pathToRandomVideo = config.get('path', 'pathToRandomVideo')
TOKEN = config.get('api', 'TOKEN')
waitForNextMessage = 1
commands = commands.commands

def help_command(update: Update, context: CallbackContext) -> None:
    if db.checkUserExist == 0:
        logicForCommand.sign(update.message.from_user)
    else:        
        logicForCommand.updateUser(update.message.from_user)

    update.message.reply_text(logicForCommand.getHelpMessage())

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def photo(update: Update, context: CallbackContext) -> None:
    update.message.reply_photo(photo=open(pathToPhotoMemes + '/' + logicForCommand.getMemFromDisk(pathToPhotoMemes, update.message.from_user, update.message.text), 'rb'))

def champ(update: Update, context: CallbackContext) -> None:
    champ = logicForCommand.getChamp()
    update.message.reply_photo(caption=champ[0], photo = champ[1])

def randomTeamChamp(update: Update, context: CallbackContext) -> None:
    for x in range(5):
        champ = logicForCommand.getChamp()
        update.message.reply_photo(caption=champ[0], photo = champ[1])
        time.sleep(waitForNextMessage)

def balanceTeamChamp(update: Update, context: CallbackContext) -> None:
    team = logicForCommand.getBalancedTeam()
    champIndex = 0
    for champ in team:
        if champ != 'champsList':
            update.message.reply_photo(photo = team[champ], caption=team['champsList'][champIndex])
            champIndex = champIndex + 1
            time.sleep(waitForNextMessage)

def love(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(logicForCommand.getLove())

def video(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(logicForCommand.getVideo(update.message.from_user, update.message.text))

def rank(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(logicForCommand.rank(pathToPhotoMemes, update.message.from_user))

def sign(update: Update, context: CallbackContext) -> None:
    logicForCommand.sign(update.message.from_user)
    update.message.reply_text('Zostałeś pomyślnie dodany do rankingu.')

updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', help_command))
updater.dispatcher.add_handler(CommandHandler(commands["help"]["name"], help_command))
updater.dispatcher.add_handler(CommandHandler(commands["hello"]["name"], hello))
updater.dispatcher.add_handler(CommandHandler(commands["photo"]["name"], photo))
updater.dispatcher.add_handler(CommandHandler(commands["champ"]["name"], champ))
updater.dispatcher.add_handler(CommandHandler(commands["randomTeam"]["name"], randomTeamChamp))
updater.dispatcher.add_handler(CommandHandler(commands["balanceTeam"]["name"], balanceTeamChamp))
updater.dispatcher.add_handler(CommandHandler(commands["love"]["name"], love))
updater.dispatcher.add_handler(CommandHandler(commands["video"]["name"], video))
updater.dispatcher.add_handler(CommandHandler(commands["rank"]["name"], rank))
updater.dispatcher.add_handler(CommandHandler('sign', sign))


updater.start_polling()
updater.idle()