# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
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
gZalgoMode = False
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
                CommandHandler('addresponse', addResponse),
                CommandHandler('deleteresponse', deleteResponse),
                CommandHandler('showresponses', showResponses)]

    # Add each handler
    for handler in handlers:
        dispatcher.add_handler(handler)
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
    limit = 2000  # limit of chars for a message
    messageParts = splitStringIntoChunks(message, limit)
    if messageParts is not "":
        for messagePart in messageParts:
            actuallySendMessage(context, userID, messagePart)


def actuallySendMessage(context, userID, message):
    # should only be called by sendMessage
    forbiddenChars = [".", "!", "-"]
    if gZalgoMode:
        message = zalgo_text.zalgo.zalgo().zalgofy(message)
    if any(forbiddenChars) in message:
        context.bot.send_message(chat_id=userID,
                                 text=message,
                                 parse_mode=telegram.ParseMode.HTML)
    else:
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
    df = openPickle(responsesFileName)  # open responses
    triggerStrings = df[gResponseColumns[0]].tolist()
    responses = df[gResponseColumns[1]].tolist()

    Response = textMessage
    for triggerString in triggerStrings:
        if triggerString.lower() in textMessage.lower():  # if the detected string is in the text message
            index = triggerStrings(triggerString)
            Response = responses[index]

    if Response is not textMessage:
        sendMessage(context, userID, Response)


def setZalgo(update, context):
    global gZalgoMode
    userID = str(update.effective_chat.id)
    gZalgoMode = not gZalgoMode
    if gZalgoMode:
        response = "Scary mode enabled"
    else:
        response = "Scary mode disabled"
    sendMessage(context, userID, response)


def addResponse(update, context):
    userID = str(update.effective_chat.id)
    commandArgs = context.args
    if len(commandArgs) >= 2:
        # s = shelve.open(responsesFileName)
        df = openPickle(responsesFileName)
        newString = commandArgs.pop(0)
        newResponse = ""
        if len(newString) >= 3:
            for arg in commandArgs:
                newResponse += " " + arg
            df = df.append({gResponseColumns[0]: newString,
                            gResponseColumns[1]: newResponse},
                           ignore_index=True)
            savePickle(df, responsesFileName)
            print(df)
            sendMessage(context, userID, "New trigger word added for {}".format(newString))


def deleteResponse(update, context):
    userID = str(update.effective_chat.id)
    commandArgs = context.args
    if len(commandArgs) == 1:
        # s = shelve.open(responsesFileName)
        df = openPickle(responsesFileName)
        newString = commandArgs.pop(0)
        triggeringStrings = df[gResponseColumns[0]].tolist()
        for trigger in triggeringStrings:
            if newString == trigger:
                index = triggeringStrings.index(trigger)
                df = (df.drop([index])).reset_index()
                break
        savePickle(df, responsesFileName)
        sendMessage(context, userID, "Trigger word for {0} has been removed".format(newString))


def showResponses(update, context):
    userID = str(update.effective_chat.id)
    df = openPickle(responsesFileName)
    triggeringWords = df[gResponseColumns[0]].tolist()
    message = ":( Words that trigger me :(\n"
    for trigger in triggeringWords:
        message += trigger + "\n"
    sendMessage(context, userID, message)


# Main
setup()
config = open(configFileName).readlines()
token = str(config[0]).replace("\n", "")
admin = str(config[1]).replace("\n", "")
if __name__ == '__main__':
    main()


