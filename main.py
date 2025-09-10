#33333333333333333333333333333333333333333333333333333333
#33333333333333333333333333333333333333333333333333333333
import telebot
from currency_converter import CurrencyConverter
from telebot import types

# Создаем бота
bot = telebot.TeleBot('Token к боту')
# Переменная для суммы
amount = 0
# Объект для конвертации валют
currency = CurrencyConverter()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, рад тебя видеть! Введите сумму:")
    bot.register_next_step_handler(message, summa)  # Переход к следующему шагу

# Обработка введенной суммы
def summa(message):
    global amount
    try:
        amount = int(message.text.strip())  # Пытаемся перевести текст в число
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму числом.')
        bot.register_next_step_handler(message, summa)  # Если ошибка — просим ввести снова
        return
    
    if amount > 0:
        # Создаем кнопки выбора валют с флагами
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('🇺🇸 USD/🇪🇺 EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('🇪🇺 EUR/🇺🇸 USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('🇺🇸 USD/🇬🇧 GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('🇬🇧 GBP/🇺🇸 USD', callback_data='gbp/usd')
        btn5 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше нуля. Введите сумму ещё раз:')
        bot.register_next_step_handler(message, summa)  # Если сумма меньше нуля, просим заново

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        # Разделяем валюты
        values = call.data.upper().split('/')
        try:
            # Конвертируем валюту
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)} {values[1]}. Чтобы начать заново, введите сумму:')
            bot.register_next_step_handler(call.message, summa)  # Снова ждём сумму
        except Exception:
            bot.send_message(call.message.chat.id, 'Ошибка конвертации. Попробуйте снова.')
            bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валют через слеш (например: USD/EUR):')
        bot.register_next_step_handler(call.message, my_currency)

# Обработка ввода своих валют
def my_currency(message):
    try:
        # Разделяем введенные валюты
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)} {values[1]}. Чтобы начать заново, введите сумму:')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Введите пару валют заново в формате USD/EUR:')
        bot.register_next_step_handler(message, my_currency)
#22222222222222222222222222222222222222222222222222222222222222222222222222222222222222
# Запускаем бота22222222222222222222222222222222222222222222222222222222222222222222222
#22222222222222222222222222222222222222222222222222222222222222222222222222222222222222
#33333333333333333333333333333333333333333333333333333333333333333333333333333333333333
bot.polling(none_stop=True)
