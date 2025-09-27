import telebot
from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = (
        "Чтобы получить цену валюты, введите команду в формате:\n"
        "<имя валюты, цену которой хотите узнать> "
        "<имя валюты, в которой надо узнать цену> "
        "<количество валюты>\n\n"
        "Пример: доллар рубль 100\n\n"
        "Список доступных валют: /values"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException("Неверное количество параметров. Формат: валюта1 валюта2 количество")

        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        bot.reply_to(message, f"{amount} {base} = {total} {quote}")


bot.polling()
