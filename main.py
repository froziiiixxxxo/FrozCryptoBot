import telebot
from telebot import types
import requests

# Вставьте сюда ваш токен бота
TOKEN = '7587256412:AAGjo6mYs4pZuyuF-4zJQLk3ZNtCYQyOSDc'

bot = telebot.TeleBot(TOKEN)

# Список криптовалют с их идентификаторами на CoinGecko
cryptos = {
    'Bitcoin': 'bitcoin',
    'Ethereum': 'ethereum',
    'Dogecoin': 'dogecoin',
    'TRON': 'tron',
    'Notcoin': 'notcoin',
    'Tether': 'tether',
    'Pepe': 'pepe',
    'Litecoin': 'litecoin',
    'Ripple': 'ripple'
}

help = """Сообщить об ошибке - @frozziiii_bot
Связь с владельцем - @frozziiii_bot"""

commands = """/commands - список команд✏
/rate - курс криптовалют
/start - перезапуск
/help - помощь"""


#СТАРТ
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Узнать курс', callback_data='rate')
    btn2 = types.InlineKeyboardButton('Помощь', callback_data='help')
    markup.add(btn1, btn2)

    bot.reply_to(message, "Привет! Используй кнопку ниже чтобы узнать текущие курсы криптовалют💸",
                 reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'rate':
            # Обработка нажатия на кнопку "Узнать курс"
            try:
                ids = ','.join(cryptos.values())
                url = 'https://api.coingecko.com/api/v3/simple/price'
                params = {
                    'ids': ids,
                    'vs_currencies': 'usd,rub'
                }
                response = requests.get(url, params=params)
                data = response.json()

                message_lines = []
                for name, id in cryptos.items():
                    price_info = data.get(id)
                    if price_info:
                        usd_price = price_info.get('usd', 'N/A')
                        rub_price = price_info.get('rub', 'N/A')
                        message_lines.append(f"{name}:  ${usd_price}  /  ₽{rub_price}")
                    else:
                        message_lines.append(f"{name}: Данные недоступны")
                    # добавляем пустую строку между криптовалютами
                    message_lines.append('')
                reply_text = "\n".join(message_lines)
                bot.send_message(call.message.chat.id, reply_text)
            except Exception as e:
                bot.send_message(call.message.chat.id, "Произошла ошибка при получении данных. Попробуйте позже.")
        elif call.data == 'help':
            bot.send_message(call.message.chat.id, help)
        else:
            bot.send_message(call.message.chat.id, "Неизвестная команда.")


#СТОИМОСТЬ
@bot.message_handler(commands=['rate'])
def handle_course(message):
    try:
        ids = ','.join(cryptos.values())
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': ids,
            'vs_currencies': 'usd,rub'
        }
        response = requests.get(url, params=params)
        data = response.json()

        message_lines = []
        for name, id in cryptos.items():
            price_info = data.get(id)
            if price_info:
                usd_price = price_info.get('usd', 'N/A')
                rub_price = price_info.get('rub', 'N/A')
                message_lines.append(f"{name}:  ${usd_price}  /  ₽{rub_price}")
            else:
                message_lines.append(f"{name}: Данные недоступны")
                #пустая строка между криптовалютами
            message_lines.append('')

        reply_text = "\n".join(message_lines)
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при получении данных. Попробуйте позже.")


#ПОМОЩЬ
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, help)


#КОМАНДЫ
@bot.message_handler(commands=['commands'])
def handle_help(message):
    bot.reply_to(message, commands)


if __name__ == '__main__':
    print('Бот запущен')
    bot.polling()