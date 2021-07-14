# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
import time

import telegram
import zalgo_text.zalgo
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
import zalgo_text
import pandas as pd

# TODO
# Add /help to list the commands
# figure out the restart option
# edit README

# GLOBALS
gZalgoMode = [False, None]  # [Is Zalgo Mode, UserID]
gShutTheFuckingFuckUp = False
gResponseColumns = ["Detect String", "Response"]
configFileName = "configuration.txt"
responsesFileName = "responses.p"


def setup():
    if not os.path.isfile(configFileName):
        print("creating config file...")
        configFile = open(configFileName, "w+")  # create config file
        configFile.write("Replace_me_with_the_telegram_token\n")
        configFile.write("Optionally_replace_me_with_UserID_of_the_developer")
        configFile.close()
        print("done!\n")
    if not os.path.isfile(responsesFileName):
        print("creating responses file...")
        # add default responses
        data = [["sticky", "I can make your mother sticky"],
                ["wet", "Your mother was wet"],
                ["gay", "Your mother is gay"],
                ["big", "Hah, that's what she said"]]
        df = pd.DataFrame(data=data, columns=gResponseColumns)
        df.to_pickle(responsesFileName)
        print("done!\n")


def main():
    print("starting...")
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    handlers = [MessageHandler(Filters.text & (~Filters.command), messageHandler),
                CommandHandler('start', start),
                CommandHandler('scary', setZalgo),
                CommandHandler('shut', shut),
                CommandHandler('addresponse', addResponse)]
    # Add each handler
    for i in range(len(handlers)):
        dispatcher.add_handler(handlers[i])
    updater.start_polling()
    print("started")


def splitStringIntoChunks(string, limit):
    # Where string is the long string and limit is how many chars
    chunks = [string[i:i + limit] for i in range(0, len(string), limit)]
    return chunks


def openPickle(fileName):
    return pd.read_pickle(fileName)


def savePickle(df, fileName):
    pd.to_pickle(df, filepath_or_buffer=fileName)


def sendMessage(context, userID, message):
    message = message.replace(".", "").replace("!", "").replace("-", "")  # remove all '.' and '!'
    if gZalgoMode[0] and gZalgoMode[1] == userID:
        message = zalgo_text.zalgo.zalgo().zalgofy(message)
    else:
        message = message.replace(".", "")
    try:
        context.bot.send_message(chat_id=userID,
                                 text=message,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    except Exception as e:
        print(e)
        # Basically, sometimes special characters aren't accepted
        # So change the formatting and try again
        context.bot.send_message(chat_id=userID,
                                 text=message,
                                 parse_mode=telegram.ParseMode.HTML)


# Telegram command/message handlers
def start(update, context):
    userID = str(update.effective_chat.id)
    sendMessage(context, userID, "yo, i am bot, nice chu meat u")


def messageHandler(update, context):
    userID = str(update.effective_chat.id)  # update.effective_chat.id is the chat id
    textMessage = update.message.text  # update.message.text is the message that user sent
    # Handles the general messages
    df = openPickle(responsesFileName)  # open responses
    detectStrings = df[gResponseColumns[0]].tolist()
    responses = df[gResponseColumns[1]].tolist()
    Response = textMessage
    for i in range(len(detectStrings)):
        if detectStrings[i].lower() in textMessage.lower():  # if the detected string is in the text message
            Response = responses[i]

    if not gShutTheFuckingFuckUp or Response is not textMessage:
        limit = 2000  # limit of chars for a message
        messageParts = splitStringIntoChunks(Response, limit)
        for i in range(len(messageParts)):
            sendMessage(context, userID, messageParts[i])
            time.sleep(0.5)  # so as to not overload it


def setZalgo(update, context):
    global gZalgoMode
    userID = str(update.effective_chat.id)
    gZalgoMode = [(not gZalgoMode[0]), userID]
    if gZalgoMode[0]:
        response = "Scary mode enabled"
    else:
        response = "Scary mode disabled"
    sendMessage(context, userID, response)


def shut(update, context):
    global gShutTheFuckingFuckUp
    userID = str(update.effective_chat.id)
    gShutTheFuckingFuckUp = not gShutTheFuckingFuckUp

    if gShutTheFuckingFuckUp:
        Response = "Okay mom"
    else:
        Response = "I believe in freedom of speech"
    sendMessage(context, userID, Response)


def addResponse(context, update):
    # userID = str(update.effective_chat.id)
    commandArgs = update.args
    if len(commandArgs) >= 2:
        df = openPickle(responsesFileName)
        newString = commandArgs.pop(0)
        newResponse = ""
        for i in range(len(commandArgs)):
            newResponse += " " + commandArgs[i]

        df = df.append({gResponseColumns[0]: newString,
                       gResponseColumns[1]: newResponse},
                       ignore_index=True)
        savePickle(df, responsesFileName)
        print("")
        print(df)
        print("")


# Main
setup()
config = open(configFileName).readlines()
token = str(config[0]).replace("\n", "")
admin = str(config[1]).replace("\n", "")
if __name__ == '__main__':
    main()


