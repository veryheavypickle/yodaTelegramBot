# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

import telegram
import zalgo_text.zalgo
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
from datetime import date
import zalgo_text

# TODO
# Add /help to list the commands
# figure out the restart option
# edit README

# GLOBALS
gZalgoMode = [False, None]  # [Is Zalgo Mode, UserID]
configFileName = "configuration.txt"


def setup():
    if not os.path.isfile(configFileName):
        print("creating config file...")
        configFile = open(configFileName, "w+")  # create config file
        configFile.write("Replace_me_with_the_telegram_token\n")
        configFile.write("Optionally_replace_me_with_UserID_of_the_developer")
        configFile.close()
        print("done!\n")


def main():
    print("starting...")
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    handlers = [MessageHandler(Filters.text & (~Filters.command), messageHandler),
                CommandHandler('start', start),
                CommandHandler('scary', setZalgo)]
    # Add each handler
    for i in range(len(handlers)):
        dispatcher.add_handler(handlers[i])
    updater.start_polling()
    print("started")


def sendMessage(context, userID, message):
    message = message.replace(".", "").replace("!", "")  # remove all '.' and '!'
    if gZalgoMode[0] and gZalgoMode[1] == userID:
        message = zalgo_text.zalgo.zalgo().zalgofy(message)
    else:
        message = message.replace(".", "")
    context.bot.send_message(chat_id=userID,
                             text=message,
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)


# Telegram command/message handlers
def start(update, context):
    userID = str(update.effective_chat.id)
    sendMessage(context, userID, "yo, i am bot, nice chu meat u")


def messageHandler(update, context):
    userID = str(update.effective_chat.id)  # update.effective_chat.id is the chat id
    textMessage = update.message.text  # update.message.text is the message that user sent
    # Handles the general messages
    Response = textMessage
    if "big" in textMessage:
        Response = "Hah, that's what she said"
    elif "gay" in textMessage:
        Response = "Your mother is gay"

    sendMessage(context, userID, Response)
    print("User: {0}\nResponse: {1}\n".format(textMessage, Response))


def setZalgo(update, context):
    global gZalgoMode
    userID = str(update.effective_chat.id)
    gZalgoMode = [(not gZalgoMode[0]), userID]
    if gZalgoMode[0]:
        response = "Scary mode enabled"
    else:
        response = "Scary mode disabled"
    sendMessage(context, userID, response)


# Main
setup()
config = open(configFileName).readlines()
token = str(config[0]).replace("\n", "")
admin = str(config[1]).replace("\n", "")
if __name__ == '__main__':
    main()

