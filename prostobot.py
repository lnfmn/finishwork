import telebot
from extensions import APIException, Convertor
from confing import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<евро (в данной подписке доступна конвертация в евро)> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        if values[0] == 'евро':
           answer = Convertor.get_price(*values)
        else:
            raise APIException('Введите первой валюту в евро.')

    except APIException as e:
        bot.reply_to(message, f"ошибка ввода:\n{e}")

    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()