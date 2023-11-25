import telebot
from config import TOKEN, keys
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def help(message: telebot.types.Message):
    text = ('Для начала работы введите команду для бота в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \
\nУвидеть список доступных валют - введите команду /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите запрос корректно!')

        quote, base, amount = values
        data = Converter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')

    else:
        text = f'Цена {amount} "{quote}" в "{base}" - {data}'
        bot.send_message(message.chat.id, text)

# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'hello')


bot.polling()
