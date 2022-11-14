import telebot
from config import currency, TOKEN
from extensions import APIException, Convertor



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def description(message):
    bot.send_message(message.chat.id, f"Добро пожаловать в Currency Bot, {message.chat.username} 😏!\n\n"
                                      f"Для работы со мной необходимо ввести следующие параметры ⚙️:\n<имя валюты цену который вы хотите узнать> \n<имя валюты в которой надо узнать цену первой валюты> \n<количество первой валюты>\n\n"
                                      f"Например, <рубль> <доллар> <1000>\n"
                                      f"Список доступных валют можно найти здесь: /values")

@bot.message_handler(commands=['values'])
def description_val(message):
    text = 'Доступные валюты:\n'
    for i in currency.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = Convertor.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()




