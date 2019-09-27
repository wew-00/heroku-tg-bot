import telebot
import const
from telebot import types
from geopy.distance import vincenty

API_TOKEN = '886849554:AAFbuhXN1f3qm36Uz-lDX7o01wWVQR6-_0c'

LIBRARY = ({
               'title': 'ХПИ библиотка',
               'lonm': 36.249873,
               'latm': 49.999177,
               'address': 'г.Харьков , у. Кирпичова, д. 2'
           }, {
               'title': 'ХПИ библиотка',
               'lonm': 49.999177,
               'latm': 36.249873,
               'address': 'г.Харьков , у. Рымарская, д. 2'
           })

bot = telebot.TeleBot(API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_lib = types.KeyboardButton('ХПИ библиотека', request_location=True)
btn_subject = types.KeyboardButton('Предметы')
btn_delivery = types.KeyboardButton('Что-то')
markup_menu.add(btn_lib, btn_delivery, btn_subject)

markup_inline_math = types.InlineKeyboardMarkup(row_width=1)
btn_in_math_logic = types.InlineKeyboardButton('Математическая логика', callback_data='math_logic')
btn_in_math_discrete = types.InlineKeyboardButton('Дискретная математика', callback_data='math_discrete')
btn_in_math_analysis = types.InlineKeyboardButton('Математический анализ', callback_data='math_analysis')
btn_in_programming = types.InlineKeyboardButton('Тер Вер', callback_data='teor_ver')
btn_in_differential_equations = types.InlineKeyboardButton('Дифференциальные уравнения', callback_data='kurpa')

markup_inline_math.add(btn_in_math_logic, btn_in_math_discrete, btn_in_math_analysis, btn_in_programming,
                       btn_in_differential_equations)

markup_inline_programming = types.InlineKeyboardMarkup(row_width=1)
btn_c = types.InlineKeyboardButton('C/C++', callback_data='c_c++')
btn_python = types.InlineKeyboardButton('Python', callback_data='python')
btn_net = types.InlineKeyboardButton('C#/.NET', callback_data='c#_net')
btn_java = types.InlineKeyboardButton('Java', callback_data='java')
markup_inline_programming.add(btn_c, btn_python, btn_net, btn_java)

markup_inline_additionally = types.InlineKeyboardMarkup(row_width=1)
btn_philosophy = types.InlineKeyboardButton('Философия', callback_data='philosophy')
btn_history = types.InlineKeyboardButton('История Украины', callback_data='history')
btn_culture = types.InlineKeyboardButton('История Украинской Культуры', callback_data='culture')
markup_inline_additionally.add(btn_philosophy, btn_history, btn_culture)

markup_additionally = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_add_math = types.KeyboardButton('Математика')
btn_add_additionally = types.KeyboardButton('Дополнительные предметы')
btn_add_programming = types.KeyboardButton('Программирование')

markup_additionally.add(btn_add_additionally, btn_add_programming, btn_add_math)

subject = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_1 = types.KeyboardButton('Математический анализ')
btn_2 = types.KeyboardButton('Дифуры')
btn_3 = types.KeyboardButton('Математическая логика')

subject.add(btn_1, btn_2, btn_3)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот КМПС", reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)
    if message.text == "Что-то":
        bot.reply_to(message, "Загадочное", reply_markup=markup_menu)
    elif message.text == "Предметы":
        bot.reply_to(message, "Выберете предмет ", reply_markup=markup_additionally)
    elif message.text == "Математика":
        bot.reply_to(message, "Выберете дисцеплину :", reply_markup=markup_inline_math)
    elif message.text == "Программирование":
        bot.reply_to(message, "Выберете дисцеплину :", reply_markup=markup_inline_programming)
    elif message.text == "Дополнительные предметы":
        bot.reply_to(message, "Выберете дисцеплину :", reply_markup=markup_inline_additionally)
    else:
        bot.reply_to(message, message.text, reply_markup=markup_menu)


# @bot.message_handler(func=lambda message: True)
# def echo_additionally(message):
#    if message.text == "Математика":
#        bot.reply_to(message, "Математический анализ", reply_markup=subject)
#    else:
#        print("error")


@bot.message_handler(func=lambda message: True, content_types=['location'])
def lib_location(message):
    print(message)
    lat = message.location.latitude
    lon = message.location.longitude

    print('Широта {} долгота {}'.format(lat, lon))

    distance = []
    for m in LIBRARY:
        result = vincenty((m['latm'], m['lonm']), (lat, lon)).kilometers
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Ближайшая к вам библтотека')
    bot.send_venue(message.chat.id,
                   const.LIBRARY[index]['latm'],
                   const.LIBRARY[index]['lonm'],
                   const.LIBRARY[index]['title'],
                   const.LIBRARY[index]['address']
                   )


@bot.callback_query_handler(func=lambda call: True)
def call_back_math(call):
    print(call)
    if call.data == 'math_logic':
        bot.send_message(call.message.chat.id, text="""
        https://ru.wikipedia.org/wiki/Математическая_логика
        """, reply_markup=markup_inline_math)  # reply_markup=markup_inline_payment
    elif call.data == 'math_discrete':
        bot.send_message(call.message.chat.id, text="""
        https:// ru.wikipedia.org/wiki/Дискретная_математика
        """, reply_markup=markup_inline_math)
    elif call.data == 'math_analysis':
        bot.send_message(call.message.chat.id, text="""
        https://my.pcloud.com/publink/show?code=XZsT4z7Z56kLu4nAwfXpSDWQH5Rm78FE8o1y
        """, reply_markup=markup_inline_math)
    elif call.data == 'teor_ver':
        bot.send_message(call.message.chat.id, text="""
        https://my.pcloud.com/publink/show?code=XZwl4z7ZpJPucn2Ixu7FD29bmwWxkRsMMEuV
        """, reply_markup=markup_inline_math)
    elif call.data == 'kurpa':
        bot.send_message(call.message.chat.id, text="""
        https://my.pcloud.com/publink/show?code=XZlP4z7ZN8TEAy8aDwmC5rSenROLoF2uTuL7
        """),
        bot.send_message(call.message.chat.id, text="""
        https://my.pcloud.com/publink/show?code=XZUP4z7ZFuYKnl6w7CY7qFYuzv1FH0oyDF7V
        """, reply_markup=markup_inline_math)
    elif call.data == 'c_c++':
        bot.send_message(call.message.chat.id, text="""
        https://tproger.ru/books/cpp-books-beginners/
        """, reply_markup=markup_inline_programming)
    elif call.data == 'python':
        bot.send_message(call.message.chat.id, text="""
        https://proglib.io/p/python-best-books/
        """, reply_markup=markup_inline_programming)
    elif call.data == 'java':
        bot.send_message(call.message.chat.id, text="""
        https://proglib.io/p/java-books-2019/
        """, reply_markup=markup_inline_programming)
    elif call.data == 'c#_net':
        bot.send_message(call.message.chat.id, text="""
        https://proglib.io/p/best-programming-books/
        """, reply_markup=markup_inline_programming)
    elif call.data == 'philosophy':
        bot.send_message(call.message.chat.id, text="""
        https://cameralabs.org/11136-15-vazhnykh-knig-po-filosofii-i-sotsialnym-naukam-chtoby-prokachat-v-sebe-gumanitariya
        """, reply_markup=markup_inline_additionally)
    elif call.data =='history':
        bot.send_message(call.message.chat.id, text="""
        https://ru.espreso.tv/article/2017/07/21/15_knyg_kotorye_luchshe_vsego_rasskazhut_ystoryyu_ukrayny
        """, reply_markup=markup_inline_additionally)
    elif call.data =='culture':
        bot.send_message(call.message.chat.id, text="""
               http://dspace.zsmu.edu.ua/bitstream/123456789/1043/1/%D0%A2%D1%83%D1%80%D0%B3%D0%B0%D0%BD%20%D0%93%D0%B0%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%A1%D0%B8%D0%B4%D0%BE%D1%80%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%98%D0%A3%D0%9A.pdf
        """, reply_markup=markup_inline_additionally)


bot.polling()

# http://tlgrm.ru/docs/bots/api
#
