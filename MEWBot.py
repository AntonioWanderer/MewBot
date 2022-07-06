import telebot
import Config
import random
from telebot import types
import datetime

grad = 0
tm = datetime.datetime.now()

bot = telebot.TeleBot(Config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("Покажи мне котика!")
    item2 = types.KeyboardButton("Определи какой я котик")
    item3 = types.KeyboardButton("Покормить")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Мур, {0.first_name}!\n я - <b>{1.first_name}</b>, твой цифровой кот (и моя миска опять пуста!)  \n Что ты там хомячишь? Поделись? ".format(message.from_user, bot.get_me()),
                     parse_mode = 'html', reply_markup = markup)
    sti = open('intro.jpg', 'rb')
    bot.send_sticker(message.chat.id, sti)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Покажи мне котика!':
            pass
            n = random.randint(1, 25)
            num = "Show\\" + str(n) + ".jpg"
            sti = open(num, 'rb')
            bot.send_sticker(message.chat.id, sti)
        elif message.text == 'Определи какой я котик':
            bot.send_message(message.chat.id, "К сожалению, функция в разработке, а автор путешествует( Но он обещал вернуться и запрограммировать тест на котика")
            n = random.randint(1, 5)
            num = "Sad\\" + str(n) + ".jpg"
            sti = open(num, 'rb')
            bot.send_sticker(message.chat.id, sti)
            #markup = types.InlineKeyboardMarkup(row_width = 2)
            #item1 = types.InlineKeyboardButton("Good", callback_data = 'good')
            #item2 = types.InlineKeyboardButton("Bad", callback_data = 'bad')
            #markup.add(item1, item2)
            
            #bot.send_message(message.chat.id, "I'm fine, and you?", reply_markup = markup)
        #else:
            #bot.send_message(message.chat.id, "I dont know this command")
        elif message.text == 'Покормить':
            markup = types.InlineKeyboardMarkup(row_width = 2)
            item1 = types.InlineKeyboardButton("Кормом", callback_data = 'pack')
            item2 = types.InlineKeyboardButton("Мясом", callback_data = 'meat')
            item3 = types.InlineKeyboardButton("Травой", callback_data = 'grass')
            markup.add(item1, item2, item3)
            
            bot.send_message(message.chat.id, "Чем покормишь? Мрр", reply_markup = markup)
    
@bot.callback_query_handler(func = lambda call: True)
def callback_infine(call):
    pack1 = ["Оо! Мрр, спасибо!", "Вкуснотища!", "А можно ещё?", "Отличный корм", "Вкусно, но мало"]
    pack2 = ["Мяв, наелся", "Ещё? Нуу.. Давай", "Дай погрызть огурца теперь", "(еле дышит)", "Это лучше чем вские ваши мыши"]
    pack3 = ["Неее", "(воротит нос от миски)", "Спасибо, не сейчас", "Я же лопну", "Оставь здесь, потом доем"]
    meat1 = ["Сссочное!", "Мряяу! Добыча!", "Премного благодарен", "Это всё мне? Правда??", "(жадно ест)"]
    meat2 = ["Добавка лишней не бывает", "Давай ещё, да", "Мммясо, ррр", "Можно ещё немного", "(Поел и жадно смотрит)"]
    meat3 = ["(Вяло облизывает кусок мяса)", "Потом... поспать тоже надо", "(уснул носом в миску)", "Я тигл, но не бездонный", "(тяжёлое дыхание)"]
    grass1 = ["Мм, витамины!", "Зелёная... И странная", "Хозяин, зачем ты нарвал травы?", "(обнюхивает)", "Покусаю, интересная"]
    grass2 = ["Да ну, трава?", "И где ты взял эти странные зелёные штуки?", "Это еда??", "Мяя(", "Не, спасибо"]
    grass3 = ["Серьёзно???", "Мне её растаскать по полу?", "(обиженное сопение)", "(вялое обнюхивание)", "(непонимающий ор)"]
    try:
        if call.message:
            nm = random.randint(0, 4)
            if call.data == 'pack':
                if grad < 2:
                    bot.send_message(call.message.chat.id, pack1[nm])
                elif grad == 2:
                    bot.send_message(call.message.chat.id, pack2[nm])
                elif grad == 3:
                    bot.send_message(call.message.chat.id, pack3[nm])
                    bot.send_message(call.message.chat.id, "Подсказка: ваш котик сыт, приходите позже. Через 5 минут он оголодает а через 10 натурально озвереет!")
                chLvl()
            elif call.data == 'meat':
                if grad < 2:
                    bot.send_message(call.message.chat.id, meat1[nm])
                elif grad == 2:
                    bot.send_message(call.message.chat.id, meat2[nm])
                elif grad == 3:
                    bot.send_message(call.message.chat.id, meat3[nm])
                    bot.send_message(call.message.chat.id, "Подсказка: ваш котик сыт, приходите позже. Через 5 минут он оголодает а через 10 натурально озвереет!")
                chLvl()
            elif call.data == 'grass':
                if grad < 2:
                    bot.send_message(call.message.chat.id, grass1[nm])
                elif grad == 2:
                    bot.send_message(call.message.chat.id, grass2[nm])
                elif grad == 3:
                    bot.send_message(call.message.chat.id, grass3[nm])
                    bot.send_message(call.message.chat.id, "Подсказка: ваш котик сыт, приходите позже. Через 5 минут он оголодает а через 10 натурально озвереет!")
                chLvl()
    except Exception as e:
        print(repr(e))
    
def chLvl():
    global grad
    global tm
    if grad < 3:
        grad = grad + 1
    now = datetime.datetime.now()
    a = int(((now.day * 24) + now.hour) * 60 + now.minute)
    b = int(((tm.day * 24) + tm.hour) * 60 + tm.minute)
    diff = a - b 
    if diff > 15:
        mn = 3
    elif diff > 10:
        mn = 2
    elif diff > 5:
        mn = 1
    else:
        mn = 0
    if grad - mn < 0:
        grad = 0
    else:
        grad = grad - mn
    if mn > 0:
        tm = now
    #print(diff)
    #print(grad)
#Run
bot.polling(none_stop = True)
