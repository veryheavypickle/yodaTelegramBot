#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
# Program bot so that everytime a message is sent, it sends one line from the script of the Bee Movie

import random
from cleverbot_free.cbapi import CleverBot
cb = CleverBot()
cb.init()

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def bee(update, context):
    # There are 4566 lines in the script for bee movie
    numLines = 4565
    message = update.message.text  # what the user sent
    file = open("resources/bee.txt", 'r')
    script = file.readlines()
    response = ""
    while len(response) <= 4:
        response = script[random.randint(0, numLines)]
    update.message.reply_text(response)
    print("Message: {}".format(message))
    print("Response: {}".format(response))


def cleverbot(update, context):
    message = update.message.text
    directedToBot = False   # if message is directed to bot
    if update.message.chat.type == "private":
        directedToBot = True
    elif update.message.reply_to_message is not None:
        directedToBot = True

    listOfAcceptedNames = [" rectal", " Rectal", "rectal ", "Rectal ", " @RectalBot", "@RectalBot "]
    for i in range(len(listOfAcceptedNames) - 1):
        if listOfAcceptedNames[i] in message:
            message = message.replace(listOfAcceptedNames[i], "")
            directedToBot = True

    if directedToBot:
        response = cb.getResponse(message)
        update.message.reply_text(response)
        print("Message: {}".format(message))
        print("Response: {}".format(response))


def test(update, context):
    print(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("beep... boop... i am retarded and have run into an error")


def main():
    updater = Updater("TelegramToken", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, cleverbot))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
