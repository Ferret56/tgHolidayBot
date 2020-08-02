import telebot
from telebot.types import Message
import logging

from app.config import token
from app.utils import messages
from app.service.holiday import HolidayService, CountryNotFoundException, HolidayNotFoundException, \
    HolidayServiceException

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    logging.info({'message_received': {'chat_id': message.chat.id,
                                       'message': message.text}})
    bot.send_message(message.chat.id, messages.WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def help_message(message: Message):
    logging.info({'message_received': {'chat_id': message.chat.id,
                                       'message': message.text}})
    bot.send_message(message.chat.id, messages.HELP_MESSAGE)


@bot.message_handler(content_types=['text'])
def send_holiday_by_country(message: Message):
    logging.info({'message_received': {'chat_id': message.chat.id,
                                       'message': message.text}})
    try:
        holiday_data = HolidayService.get_current_holiday_in_country(message.text)
        bot.send_message(message.chat.id, 'Дата: {}\nПраздник: {}'
                         .format(holiday_data.get('date'),
                                 holiday_data.get('title')))
    except CountryNotFoundException:
        logging.warning({'message_send': {'chat_id': message.chat.id,
                                          'sender_text': message.text,
                                          'message': messages.COUNTRY_NOT_FOUND_MESSAGE}})
        bot.send_message(message.chat.id, messages.COUNTRY_NOT_FOUND_MESSAGE)
    except HolidayNotFoundException:
        logging.warning({'message_send': {'chat_id': message.chat.id,
                                          'sender_text': message.text,
                                          'message': messages.HOLIDAY_NOT_FOUND_MESSAGE}})
        bot.send_message(message.chat.id, messages.HOLIDAY_NOT_FOUND_MESSAGE)
    except HolidayServiceException as ex:
        logging.error({'message_send': {'chat_id': message.chat.id,
                                        'sender_text': message.text,
                                        'message': messages.SERVICE_ERROR},
                       'error': str(ex)})
        bot.send_message(message.chat.id, messages.SERVICE_ERROR)


bot.polling()
