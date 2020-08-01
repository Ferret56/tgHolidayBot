import telebot
from telebot.types import Message
import logging

from app.config import token
from app.utils import messages

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    logging.info({'message_received': {'chat_id': message.chat.id,
                                       'message': message.text}})
    bot.send_message(message.chat.id, messages.WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def help_message(message):
    logging.info({'message_received': {'chat_id': message.chat.id,
                                       'message': message.text}})
    bot.send_message(message.chat.id, messages.HELP_MESSAGE)


bot.polling()
