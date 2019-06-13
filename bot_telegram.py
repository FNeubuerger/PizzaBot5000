#!/usr/bin/python3

# needs python-telegram-bot

from telegram.ext import Updater, CommandHandler
import time
import generate_pizza

TOKEN_FILE = "token"

def send_pizza(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text=generate_pizza.getPizzaString(generate_pizza.generate_pizza()))


token = open(TOKEN_FILE, "r").read().rstrip()
updater = Updater(token=token)

updater.dispatcher.add_handler(CommandHandler("pizza", send_pizza))

updater.start_polling()
