import telebot
from utilis import Convert, ConvertionException
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = " что бы начать работу введите команду в слудующем формате:" \
           "\nИмя валюты > в какую валюту перевести > количество." \
           "\nПример: рубль доллар 75" \
           "\nУвидеть список всех допустимых валют - /values"
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}, {text}")

@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    values = 'Доступные валюты:'
    for key in keys.keys():
       values = '\n'.join((values, key))
    bot.send_message(message.chat.id, values)

@bot.message_handler(content_types=['text'], )
def get_conversion(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')
        if len(values) < 3:
            raise ConvertionException('Слишком мало параметров')

        quote, base, amount = values
        total_base = Convert.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)