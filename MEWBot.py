import os, sys
import os.path
from requests.exceptions import ConnectionError, ReadTimeout
import telebot
import Config
import random
from telebot import types
import datetime
from icrawler.builtin import GoogleImageCrawler
import shutil

grad = {"NoUser": 0}
tm = {"NoTime": 0}
par = {"NoPar":[0, 0, 0]} #love, food, mood

bot = telebot.TeleBot(Config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("Покажи мне котика!")
    item2 = types.KeyboardButton("Определи, какой я котик")
    item3 = types.KeyboardButton("Покормить")
    item4 = types.KeyboardButton("Мемы про котов")
    item5 = types.KeyboardButton("Рекомендовать мем")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Мур, {0.first_name}!\n я - <b>{1.first_name}</b>, твой цифровой кот (и моя миска опять пуста!)  \n Что ты там хомячишь? Поделись? ".format(message.from_user, bot.get_me()),
                     parse_mode = 'html', reply_markup = markup)
    sti = open('intro.jpg', 'rb')
    bot.send_sticker(message.chat.id, sti)

    Ub = open('UserDialogsBase.txt', 'a')
    Ub.write(str(getName(message)) + '\n')
    Ub.close()

    grad[getName(message)] = 0
    tm[getName(message)] = datetime.datetime.now()
    par[getName(message)] = [0, 0, 0]

    Hist = open('AllActivityHistory.txt', 'a')
    Hist.write(str(datetime.datetime.now()) + " " + getNameUser(message) + " New user" + '\n')
    Hist.close()

@bot.message_handler(content_types=['photo', 'document', 'video'])
def addMem(message):
    Hist = open('AllActivityHistory.txt', 'a')
    Hist.write(str(datetime.datetime.now()) + " " + getNameUser(message) + " New content №" + str(len(os.listdir('UserMemes/'))+1) + '\n')
    Hist.close()
    if message.content_type == "photo":
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("UserMemes/" + str(len(os.listdir('UserMemes/'))+1) + ".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

    if message.content_type == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("UserMemes/" + message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

    if message.content_type == "video":
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        #src =  file_info.file_path
        with open("UserMemes/" + str(len(os.listdir('UserMemes/'))+1) + ".mp4", 'wb') as new_file:
            new_file.write(downloaded_file)

@bot.message_handler(content_types=['text'])
def MainKeyboardHandler(message):
    Hist = open('AllActivityHistory.txt', 'a')
    Hist.write(str(datetime.datetime.now()) + " " + getNameUser(message) + " Message: " + " -- " + message.text + '\n')
    Hist.close()
    if message.chat.type == 'private':
        if message.text == 'Покажи мне котика!':
            bot.send_message(message.chat.id, "Напиши, какой должен быть кот (ласковый, безумный, дикий, пушистый и т.д.) Или что он делает")
        elif message.text == 'Определи, какой я котик':
            bot.send_message(message.chat.id, "Поехали! 6 вопросов")
            par[getName(message)] = [0, 0, 0]
            catTest(0, message)
            #print(getName(message))
        elif message.text == 'Покормить':
            markup = types.InlineKeyboardMarkup(row_width = 1)
            item1 = types.InlineKeyboardButton("Кормом", callback_data = 'pack')
            item2 = types.InlineKeyboardButton("Мясом", callback_data = 'meat')
            item3 = types.InlineKeyboardButton("Травой", callback_data = 'grass')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, "Чем покормишь? Мрр", reply_markup = markup)
        elif message.text == 'Мемы про котов':
            l = os.listdir('Memes/')
            print('Memes/' + l[random.randint(0,len(l)-1)])
            sti = open('Memes/' + l[random.randint(0,len(l)-1)], 'rb')
            bot.send_photo(message.chat.id, sti)
        elif message.text == 'Рекомендовать мем':
            bot.send_message(message.chat.id, "Просто скинь мне картинку с мемом (или видео, файл, ссылку)! Модератор просмотрит его (поржёт) и добавит в коллекцию.")
        else:
            if "http" in message.text:
                lnk = open('UserMemes/MemLinks.txt', 'a')
                lnk.write(message.text + '\n')
                lnk.close()
            else:
                if os.path.exists("CatsDownloaded/"+str(getNameUser(message))+"/"):
                    shutil.rmtree("CatsDownloaded/"+str(getNameUser(message))+"/")
                else:
                    os.chdir("CatsDownloaded/")
                    os.mkdir(str(getNameUser(message))+"/")
                    os.chdir("..")
                bot.send_message(message.chat.id, "Loaing...")
                sti = open("load.jpg", 'rb')
                bot.send_sticker(message.chat.id, sti)

                request_word = message.text + ' кот фото'
                num_pic = 5
                filters = dict(size='medium')
                ggl = GoogleImageCrawler(storage={'root_dir': 'CatsDownloaded/'+str(getNameUser(message))+"/"})
                ggl.crawl(keyword=request_word, filters = filters, max_num=num_pic)

                for img in os.listdir('CatsDownloaded/'+str(getNameUser(message))+"/"):
                    #print(img)
                    sti = open('CatsDownloaded/'+str(getNameUser(message))+"/" + img, 'rb')
                    bot.send_photo(message.chat.id, sti)

@bot.callback_query_handler(func = lambda call: True)
def callback_infine(call):
    global grad
    global par
    Hist = open('AllActivityHistory.txt', 'a')
    Hist.write(str(datetime.datetime.now()) + " " + getNameUser(call) + " Call: " + " -- " + call.message.text + " " + call.data + '\n')
    Hist.close()
    grad1 = grad[getName(call.message)]
    par1 = par[getName(call.message)]
    #print(grad)
    nm = 0
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
            #print(call.data)
            if call.data == 'pack':
                chLvl(call.message)
                nm = random.randint(0, 4)
                if grad1 < 3:
                    grad1 = grad1 + 1
                if grad1 < 2:
                    bot.send_message(call.message.chat.id, pack1[nm])
                elif grad1 == 2:
                    bot.send_message(call.message.chat.id, pack2[nm])
                elif grad1 == 3:
                    bot.send_message(call.message.chat.id, pack3[nm])
                    bot.send_message(call.message.chat.id, "Подсказка: ваш котик сыт, приходите позже. Через 5 минут он оголодает а через 10 натурально озвереет!")
            elif call.data == 'meat':
                chLvl(call.message)
                nm = random.randint(0, 4)
                if grad1 < 3:
                    grad1 = grad1 + 1
                if grad1 < 2:
                    bot.send_message(call.message.chat.id, meat1[nm])
                elif grad1 == 2:
                    bot.send_message(call.message.chat.id, meat2[nm])
                elif grad1 == 3:
                    bot.send_message(call.message.chat.id, meat3[nm])
                    bot.send_message(call.message.chat.id, "Подсказка: ваш котик сыт, приходите позже. Через 5 минут он оголодает а через 10 натурально озвереет!")
            elif call.data == 'grass':
                chLvl(call.message)
                nm = random.randint(0, 4)
                if grad1 < 3:
                    grad1 = grad1 + 1
                if grad1 < 2:
                    bot.send_message(call.message.chat.id, grass1[nm])
                elif grad1 == 2:
                    bot.send_message(call.message.chat.id, grass2[nm])
                elif grad1 == 3:
                    bot.send_message(call.message.chat.id, grass3[nm])
                    bot.send_message(call.message.chat.id, "Подсказка: ваш котик сыт, приходите позже. Через 5 минут он оголодает а через 10 натурально озвереет!")
            elif call.data == 'One1':
                par1[0] = par1[0] + 1
                catTest(1, call.message)
            elif call.data == 'One2':
                par1[1] = par1[1] + 1
                catTest(1, call.message)
            elif call.data == 'One3':
                par1[0] = par1[0] - 1
                catTest(1, call.message)
            elif call.data == 'One4':
                par1[2] = par1[2] + 2
                catTest(1, call.message)
            elif call.data == 'Two1':
                par1[1] = par1[1] + 1
                catTest(2, call.message)
            elif call.data == 'Two2':
                par1[1] = par1[1] + 2
                catTest(2, call.message)
            elif call.data == 'Two3':
                par1[1] = par1[1] - 2
                par1[2] = par1[2] + 2
                catTest(2, call.message)
            elif call.data == 'Two4':
                par1[1] = par1[1] - 1
                par1[2] = par1[2] + 1
                catTest(2, call.message)
            elif call.data == 'Three1':
                par1[0] = par1[0] - 2
                par1[2] = par1[2] + 1
                catTest(3, call.message)
            elif call.data == 'Three2':
                par1[0] = par1[0] + 2
                catTest(3, call.message)
            elif call.data == 'Three3':
                par1[1] = par1[1] + 1
                par1[2] = par1[2] + 2
                catTest(3, call.message)
            elif call.data == 'Three4':
                par1[0] = par1[0] + 1
                catTest(3, call.message)
            elif call.data == 'Four1':
                par1[0] = par1[0] + 1
                par1[1] = par1[1] + 1
                catTest(4, call.message)
            elif call.data == 'Four2':
                par1[0] = par1[0] + 2
                par1[1] = par1[1] + 1
                catTest(4, call.message)
            elif call.data == 'Four3':
                par1[1] = par1[1] + 1
                catTest(4, call.message)
            elif call.data == 'Four4':
                par1[0] = par1[0] - 2
                par1[1] = par1[1] - 1
                par1[2] = par1[2] + 1
                catTest(4, call.message)
            elif call.data == 'Five1':
                par1[0] = par1[0] + 2
                catTest(5, call.message)
            elif call.data == 'Five2':
                par1[0] = par1[0] + 1
                catTest(5, call.message)
            elif call.data == 'Five3':
                par1[0] = par1[0] - 2
                par1[2] = par1[2] + 1
                catTest(5, call.message)
            elif call.data == 'Five4':
                par1[0] = par1[0] - 1
                par1[2] = par1[2] + 1
                catTest(5, call.message)
            elif call.data == 'Six1':
                par1[0] = par1[0] + 2
                bot.send_message(call.message.chat.id, frmMsg(call))
            elif call.data == 'Six2':
                par1[1] = par1[1] + 2
                bot.send_message(call.message.chat.id, frmMsg(call))
            elif call.data == 'Six3':
                par1[0] = par1[0] - 1
                par1[2] = par1[2] + 2
                bot.send_message(call.message.chat.id, frmMsg(call))
            elif call.data == 'Six4':
                par1[2] = par1[2] + 1
                bot.send_message(call.message.chat.id, frmMsg(call))
    except Exception as e:
        print(repr(e))
    grad[getName(call.message)] = grad1
    par[getName(call.message)] = par1

def chLvl(message):
    global grad
    global tm
    tm1 = tm[getName(message)]
    grad1 = grad[getName(message)]
    now = datetime.datetime.now()
    a = int(((now.day * 24) + now.hour) * 60 + now.minute)
    b = int(((tm1.day * 24) + tm1.hour) * 60 + tm1.minute)
    diff = a - b
    if diff > 15:
        mn = 3
    elif diff > 10:
        mn = 2
    elif diff > 5:
        mn = 1
    else:
        mn = 0
    if grad1 - mn < 0:
        grad1 = 0
    else:
        grad1 = grad1 - mn
    if mn > 0:
        tm1 = now
    grad[getName(message)] = grad1
    tm[getName(message)] = tm1

def catTest(num, message):
    if num == 0:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        item1 = types.InlineKeyboardButton("Мурлычу и трусь о ногу", callback_data = 'One1')
        item2 = types.InlineKeyboardButton("Завываю, требуя еды", callback_data = 'One2')
        item3 = types.InlineKeyboardButton("Не обращаю внимания", callback_data = 'One3')
        item4 = types.InlineKeyboardButton("Ой, я же цветок уронил!", callback_data = 'One4')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Когда хозяин приходит с работы", reply_markup = markup)
    elif num == 1:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        item1 = types.InlineKeyboardButton("Пуста, я вижу дно!", callback_data = 'Two1')
        item2 = types.InlineKeyboardButton("Наполовину пуста...", callback_data = 'Two2')
        item3 = types.InlineKeyboardButton("Переверну её ночью!", callback_data = 'Two3')
        item4 = types.InlineKeyboardButton("Крошки с пола лучше", callback_data = 'Two4')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Моя миска:", reply_markup = markup)
    elif num == 2:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        item1 = types.InlineKeyboardButton("Время тыгдыка!", callback_data = 'Three1')
        item2 = types.InlineKeyboardButton("Спать с человеком", callback_data = 'Three2')
        item3 = types.InlineKeyboardButton("Проверить миску :)", callback_data = 'Three3')
        item4 = types.InlineKeyboardButton("На диван не пускают :(", callback_data = 'Three4')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Кстати, ночь:", reply_markup = markup)
    elif num == 3:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        item1 = types.InlineKeyboardButton("Какие мыши?", callback_data = 'Four1')
        item2 = types.InlineKeyboardButton("Ррр! Я их ловлю!", callback_data = 'Four2')
        item3 = types.InlineKeyboardButton("Загонят меня на стол", callback_data = 'Four3')
        item4 = types.InlineKeyboardButton("Вместе таскаем еду", callback_data = 'Four4')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "А мыши?", reply_markup = markup)
    elif num == 4:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        item1 = types.InlineKeyboardButton("Мурр! Ещё за ушком!", callback_data = 'Five1')
        item2 = types.InlineKeyboardButton("Ладно, разрешу", callback_data = 'Five2')
        item3 = types.InlineKeyboardButton("Кусь!", callback_data = 'Five3')
        item4 = types.InlineKeyboardButton("Обшерстил человека", callback_data = 'Five4')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Когда меня гладят", reply_markup = markup)
    elif num == 5:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        item1 = types.InlineKeyboardButton("Своего человека", callback_data = 'Six1')
        item2 = types.InlineKeyboardButton("Дом и миску", callback_data = 'Six2')
        item3 = types.InlineKeyboardButton("Пакостить", callback_data = 'Six3')
        item4 = types.InlineKeyboardButton("Кусать огурцы и дыню", callback_data = 'Six4')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Люблю", reply_markup = markup)

def frmMsg(call):
    global par
    par1 = par[getName(call.message)]
    if par1[0] > 0:
        s1 = 1
    else:
        s1 = -1

    if par1[1] > 0:
        s2 = 1
    else:
        s2 = -1

    if par1[2] > 4:
        s3 = 1
    else:
        s3 = 0

    #s = "Итак, вы " + s1 + s2 + s3
    s= ""
    if s1 == 1:
        if s2 == 1:
            if s3 == 1:
                s = "Любимое чучело: ты бьёшь вазы в доме но потом приходишь мириться. Ну и пусть покормят заодно!"
                sti = open('Results/chuchelo.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
            if s3 == 0:
                s = "Усатый гурман: и обниматься любишь, и вазы бить не станешь, ведь где-то там ждёт еда..."
                sti = open('Results/gurman.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
        if s2 == -1:
            if s3 == 1:
                s = "Когтистая смерть: худая и одичавшая, но тебя любят"
                sti = open('Results/smert.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
            if s3 == 0:
                s = "Фитнес-кошечка: ласковая, аккуратная, худая, идеальная"
                sti = open('Results/fitness.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
    if s1 == -1:
        if s2 == 1:
            if s3 == 1:
                s = "Самодостаточность: и поесть, и диван подрать - зачем тут хозяева?"
                sti = open('Results/sama.jpeg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
            if s3 == 0:
                s = "Тёмный комочек: ты много спишь и умываешься, тебе хорошо в своём внутреннем мире"
                sti = open('Results/komok.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
        if s2 == -1:
            if s3 == 1:
                s = "Мартовский кот: тебе пофиг даже на еду, ты ищешь романтики!"
                sti = open('Results/mart.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)
            if s3 == 0:
                s = "Тихая тень: тебя видели, но сколько дней назад - никто не помнит"
                sti = open('Results/ten.jpg', 'rb')
                bot.send_sticker(call.message.chat.id, sti)

    Hist = open('AllActivityHistory.txt', 'a')
    Hist.write(str(datetime.datetime.now()) + " " + getNameUser(call) + " Test result: " + " " + s + '\n')
    Hist.close()
    #print(par1)
    par1 = [0, 0, 0]
    par[getName(call.message)] = par1
    return(s)

def getName(message): #dialog name!
    uid = message.chat.id
    name = uid
    #print(name)
    return(name)

def getNameUser(message):
    uid = message.from_user.id
    fnm = message.from_user.first_name
    lnm = message.from_user.last_name
    unm = message.from_user.username
    name = str(uid) + " " + str(fnm) + " " + str(lnm) + " " + str(unm)
    return(name)

#Run
Hist = open('AllActivityHistory.txt', 'a')
Hist.write(str(datetime.datetime.now()) + " Restart." + '\n')
Hist.close()
Ub = open('UserDialogsBase.txt', 'r')
for line in Ub:
    grad[int(line.replace("\n",""))] = 0
    tm[int(line.replace("\n",""))] = datetime.datetime.now()
    par[int(line.replace("\n",""))] = [0, 0, 0]
Ub.close()
#print(grad)
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)