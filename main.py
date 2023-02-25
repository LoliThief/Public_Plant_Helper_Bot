# Standart libraries
from random import choice
import json, datetime, time

# Our files
# import Base
import Data
from config import TOKEN

# PIP libraries
import telebot

owner_id = #my_id was here 
send_actions = False

bot = telebot.TeleBot(TOKEN)

plants = {}

with open("content.json", encoding='ascii') as json_file:
    plants = json.load(json_file)

print('bot is ready!')

def is_admin(username):
    for admin in Data.super_usernames:
        if username == admin:
            return True
    return False

def get_user_plants(user_id = owner_id):
    user_id = str(user_id)
    user_data_dict = {}
    with open("user_data.json", 'r', encoding='ascii') as json_file:
        user_data_dict = json.load(json_file)
    if user_id in user_data_dict.keys():
        return user_data_dict[user_id]["plants"]
    else:
        return []

def add_user_plant(user_id = owner_id, plant_data = "Бонсай/Серисса"):
    user_id = str(user_id)
    user_data_dict = {}
    c = plant_data.split('/')[0]
    p = plant_data.split('/')[1]
    f = int(plants[c][p]['Частота полива'])
    with open("user_data.json", 'r', encoding='ascii') as json_file:
        user_data_dict = json.load(json_file)

    if user_id in user_data_dict.keys():
        if plant_data not in user_data_dict[str(user_id)]["plants"]:
            user_data_dict[user_id]["plants"].append(plant_data)
            user_data_dict[user_id]["f"].append(f)
    else:
        user_data_dict[user_id] = {"plants": [plant_data], 'f': [f]}
    #user_data_dict[user_id] = {"plants": ["Бонсай/Серисса", "Бонсай/Фикус священный"]}

    with open("user_data.json", 'w', encoding='ascii') as json_file:
        json.dump(user_data_dict, json_file)

def remove_user_plant(user_id = owner_id, plant_data = "Бонсай/Серисса"):
    user_id = str(user_id)
    user_data_dict = {}

    with open("user_data.json", 'r', encoding='ascii') as json_file:
        user_data_dict = json.load(json_file)

    if user_id in user_data_dict.keys():
        if plant_data in user_data_dict[user_id]["plants"]:
            for i in range(len(user_data_dict[user_id]["plants"])):
                if plant_data == user_data_dict[user_id]["plants"][i]:
                    user_data_dict[user_id]["plants"].pop(i)
                    user_data_dict[user_id]["f"].pop(i)
                    break

    with open("user_data.json", 'w', encoding='ascii') as json_file:
        json.dump(user_data_dict, json_file)

def f(message, num=10):
    a, b = 1, 1
    if num > 25:
        bot.send_message(message.chat.id, f'<b> arg is too big : (, enjoy first 50!'f' </b>', parse_mode="html")
    for i in range(min(num, 50)):
        bot.send_message(message.chat.id, f'<b> {a} </b>', parse_mode="html")
        c = a + b; a = b; b = c


def create_2_row_markup(buttons_list = [], group=0):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)

    buttons_list_1 = []
    buttons_list_2 = []

    for cur_key in buttons_list[::2]:
        btn1 = telebot.types.InlineKeyboardButton(text= cur_key[:60], callback_data= f"{group}:{cur_key[:18]}:{0}")
        buttons_list_1.append(btn1)

    for cur_key in buttons_list[1::2]:
        btn2 = telebot.types.InlineKeyboardButton(text= cur_key[:60], callback_data= f"{group}:{cur_key[:18]}:{0}")
        buttons_list_2.append(btn2)

    for i in range(min(len(buttons_list_1), len(buttons_list_2))):
        markup.add(buttons_list_1[i], buttons_list_2[i])
    if len(buttons_list_1) != len(buttons_list_2):
        markup.add(buttons_list_1[-1])

    return markup

def send_by_parts(chat_id_ = owner_id, text_ = "nigger", markup = None):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(text= "Скрыть.", callback_data=f"4:delete:")
    markup.add(btn)
    for i in range(0, (len(text_) // 4000) + 1):
        bot.send_message(chat_id=chat_id_,text=text_[i*4000:(i+1)*4000], parse_mode="html", reply_markup=markup)
    return

@bot.message_handler(commands=['start', 'f', 'help', 'set', 'ping', 'my_id', 'joke', 'notify'])
def commands(message):
    mtext = message.text.split()

    print(f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Asked me for {mtext[0]}!")

    global send_actions
    if send_actions == True:
        bot.send_message(owner_id, f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Asked me for {mtext[0]}!")
    
    if mtext[0] == '/notify':
        with open("user_data.json", 'r', encoding='ascii') as json_file:
            user_data_dict = json.load(json_file)
            today = int(str(datetime.date.today()).split('-')[2])
            for user_id in user_data_dict:
                fr = user_data_dict[user_id]['f'] 
                plant_name = user_data_dict[user_id]['plants']
                need_to_water = []
                msg = "" 
                for i in range(len(fr)):
                    if today % fr[i] == 0:
                        need_to_water.append(plant_name[i].split('/')[1])
                for i in range(len(need_to_water)):
                    msg += f"{i+1}){need_to_water[i]}\n"
                if len(need_to_water) != 0:
                    bot.send_message(chat_id=user_id, text=f"{choice(Data.notify)}  {msg}")
    
    if mtext[0] == '/f':
        try:
            f(message, int(mtext[1]))
        except:
            f(message, 15)
    if mtext[0] == "/start":
        #markup = telebot.types.InlineKeyboardMarkup()
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        #btn0 = telebot.types.InlineKeyboardButton(text= "Глоссарий", callback_data= ':main:')
        btn1 = telebot.types.KeyboardButton(text= "Глоссарий")
        btn2 = telebot.types.KeyboardButton(text= "Мои растения")
        #markup.add(btn0)
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, Data.Welcome_message, reply_markup=markup)

    if mtext[0] == "/my_id":
        bot.send_message(message.chat.id, message.chat.id)

    if mtext[0] == "/help":
        joke = ""
        if len(mtext) >= 2:
            if(mtext[1] == '-c' or mtext[1] == '--commands' or mtext[1] == '-a' or mtext[1] == '--all'):
                joke = "\n\nAdditional commands:\n/f - Fibonacci numbers[1; 50]\n/my_id - sends user id\n/ping - average ping\n/joke - coolest joke in the whole world!"
        bot.send_message(message.chat.id, Data.Help_message + joke)

    if (mtext[0] == "/ping"):
        bot.reply_to(message, "pong")

    if (mtext[0] == "/joke"):
        buttons = telebot.types.InlineKeyboardMarkup()
        btn0 = telebot.types.InlineKeyboardButton(text='Click here!', url='https://bit.ly/moralnight1705')
        buttons.add(btn0)
        bot.send_message(message.chat.id, "The joke", reply_markup=buttons)

    try:
        if (mtext[0] == '/set'):
            if (is_admin(message.chat.username) == False):
                bot.send_message(message.chat.id, 'Access Denied')
            elif (mtext[1] == 'save_pdf'):
                try:
                    global save_pdf
                    save_pdf = bool(int(mtext[2]))
                except:
                    save_pdf = False
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {save_pdf}')
            elif (mtext[1] == 'fast_mode'):
                try:
                    global fast_mode
                    fast_mode = bool(int(mtext[2]))
                except:
                    fast_mode = False
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {fast_mode}')
            elif (mtext[1] == 'number_of_books'):
                try:
                    global number_of_books
                    number_of_books = int(mtext[2])
                except:
                    number_of_books = 10
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {number_of_books}')
            elif (mtext[1] == 'send_actions'):
                try:
                    send_actions = bool(int(mtext[2]))
                except:
                    send_actions = False
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {send_actions}')
            elif (mtext[1] == '--help' or mtext[1] == '-h'):
                bot.send_message(message.chat.id, 'Parameters of "/set" \nsave_pdf\t[1, 0]\nnumber_of_books\t[0, 100]\nfast_mode\t[1, 0]\nsend_actions\t[1, 0]\n')
            else:
                bot.send_message(message.chat.id, 'unknown parameter of "/set, try --help" ')
    except:
        bot.send_message(message.chat.id, "Invalid syntax of /set, try --help")

@bot.message_handler()
def sft(message):
    global plants

    if message.text.lower() == 'Глоссарий'.lower():
        markup = create_2_row_markup( list( plants.keys() ) , group='0')
        bot.send_message(chat_id=message.chat.id, text = "Выбор Категории растений.", reply_markup=markup, parse_mode="html")
        return

    if message.text.lower() == 'Мои растения'.lower():
        user_id = str(message.chat.id)
        user_plants = get_user_plants(user_id)
        attr = 0
        if user_plants != None:
            cur_page = []
            for i in user_plants[:10]:
                cur_page.append(i.split('/')[1])
            markup = create_2_row_markup(cur_page, group='1')
            
            prev_btn = telebot.types.InlineKeyboardButton(text= "⬅️Пред.", callback_data=f'5:{user_id}:{int(attr)-1}')
            status_btn = telebot.types.InlineKeyboardButton(text= f"{int(attr) + 1} из {(len(user_plants) // 10) + 1}", url='https://bit.ly/moralnight1705')#, callback_data=f'{group}:{call_body}:{attr}')
            next_btn = telebot.types.InlineKeyboardButton(text= "След.➡️", callback_data=f'5:{user_id}:{int(attr)+1}')
            markup.add(prev_btn, status_btn, next_btn)    
            bot.send_message(chat_id=message.chat.id, text = "Ваши растения:", reply_markup=markup, parse_mode="html")
        else:
            bot.send_message(chat_id=message.chat.id, text = "У вас пока нет растений, вы можете добавить их себе в Глоссарии", parse_mode="html")
        return
    bot.send_message(message.chat.id, "Я не понял ваше сообщение, чтобы вернуться напишите /start!")

@bot.message_handler(content_types=['document'])
def handle_files(message):
    chat_id = message.chat.id
    global send_actions
    if (send_actions == True):
        print(message.chat.username, "Sended me file")
        bot.send_message(owner_id, f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Sended me file!")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global plants
    print(call.data)
    data = call.data.split(':')
    group = data[0]
    call_body = data[1]
    attr = data[2]

    if call_body == 'main':
        markup = create_2_row_markup( list( plants.keys() ) , group='0')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Выбор Категории растений.", reply_markup=markup, parse_mode="html")
        return

    # Вывод содержимого категорий 
    if group == '0':
        all_categories = list(plants.keys())
        for cur_category in all_categories:
            if call_body in cur_category:
                all_plants = list(plants[cur_category].keys())
                if attr == '':
                    cur_page = all_plants[:10]
                    attr = 0
                else:
                    if(attr == '-1'):
                        attr = 0
                        return
                    if(int(attr) > (len(all_plants) // 10)):
                        attr = (len(all_plants) // 10)
                        return
                    cur_page = all_plants[(int(attr))*10:(int(attr) + 1)*10]
                # print(call.data, cur_page)
                markup = create_2_row_markup(cur_page, group='1')
                
                prev_btn = telebot.types.InlineKeyboardButton(text= "⬅️Пред.", callback_data=f'{group}:{call_body}:{int(attr)-1}')
                status_btn = telebot.types.InlineKeyboardButton(text= f"{int(attr) + 1} из {(len(all_plants) // 10) + 1}", url='https://bit.ly/moralnight1705')#, callback_data=f'{group}:{call_body}:{attr}')
                next_btn = telebot.types.InlineKeyboardButton(text= "След.➡️", callback_data=f'{group}:{call_body}:{int(attr)+1}')
                markup.add(prev_btn, status_btn, next_btn)
                btn = telebot.types.InlineKeyboardButton(text= "↩️Назад к Категориям↩️", callback_data=':main:')
                markup.add(btn)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Категория: {call_body}.", reply_markup=markup)
                return

    # Вывод Свойств растения  
    if group == '1':
        all_categories = list(plants.keys())
        for category in all_categories:
            all_plants = list(plants[category].keys())
            for cur_plant in all_plants:
                if call_body in cur_plant:
                    markup = telebot.types.InlineKeyboardMarkup()
                    cnt = 0
                    for inf in plants[category][cur_plant].keys():
                        #print(inf)
                        if inf == 'name':
                            cnt += 1
                            continue
                        btn = telebot.types.InlineKeyboardButton(text= inf, callback_data= f"2:{call_body}:{cnt}")
                        markup.add(btn)
                        cnt += 1
                    my_plants = get_user_plants(user_id=call.message.chat.id)
                    if not f"{category}/{cur_plant}" in my_plants:
                        btn = telebot.types.InlineKeyboardButton(text= "Добавить к себе.", callback_data=f"6:{all_categories.index(category)}:{all_plants.index(cur_plant)}")
                    else:
                        btn = telebot.types.InlineKeyboardButton(text= "Удалить из моих.", callback_data=f"7:{all_categories.index(category)}:{all_plants.index(cur_plant)}")
                    markup.add(btn)
                    my = telebot.types.InlineKeyboardButton(text= "К моим растениям", callback_data=f'5:{call.message.chat.id}:{0}')
                    markup.add(my)
                    btn = telebot.types.InlineKeyboardButton(text= "↩️Назад к Категории↩️", callback_data=f"0:{category}:")
                    markup.add(btn)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Растение: {call_body}.", reply_markup=markup)
                    return 

    # Вывод Определеннго Свойства растения 
    if group == '2':
        for category in plants:
            for cur_plant in plants[category]:
                #print(cur_plant)
                if call_body in cur_plant:
                    requested_property = list(plants[category][cur_plant].keys())[int(attr)]
                    markup = telebot.types.InlineKeyboardMarkup()
                    btn = telebot.types.InlineKeyboardButton(text= "Назад", callback_data=f"1:{cur_plant[:18]}:")
                    markup.add(btn)
                    #print(list(plants[category][cur_plant].keys())[2])
                    if type(plants[category][cur_plant][requested_property]) == str:
                        send_by_parts(call.message.chat.id, f"<b>{requested_property}</b>:\n{plants[category][cur_plant][requested_property]}")
                    if type(plants[category][cur_plant][requested_property]) == int:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{cur_plant} {choice(Data.poliv)} {plants[category][cur_plant][requested_property]} дней", reply_markup=markup)
                    return

    if group == '4':# удаление сообщения!
        bot.delete_message(call.message.chat.id, call.message.message_id)

    if group == '5':
        user_id = str(call.message.chat.id)
        user_plants = get_user_plants(user_id)
        if user_plants != []:
            cur_page = []
            if attr == '-1' or int(attr) > (len(user_plants) // 10):
                return 

            for i in user_plants[(int(attr))*10:(int(attr) + 1)*10]:
                cur_page.append(i.split('/')[1])
            markup = create_2_row_markup(cur_page, group='1')
            
            prev_btn = telebot.types.InlineKeyboardButton(text= "⬅️Пред.", callback_data=f'5:{user_id}:{int(attr)-1}')
            status_btn = telebot.types.InlineKeyboardButton(text= f"{int(attr) + 1} из {(len(user_plants) // 10) + 1}", url='https://bit.ly/moralnight1705')#, callback_data=f'{group}:{call_body}:{attr}')
            next_btn = telebot.types.InlineKeyboardButton(text= "След.➡️", callback_data=f'5:{user_id}:{int(attr)+1}')
            markup.add(prev_btn, status_btn, next_btn)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Ваши растения:", reply_markup=markup, parse_mode="html")
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "У вас пока нет растений, вы можете добавить их себе в Глоссарии", parse_mode="html")
        return

    if group == '6':
        all_categories = list(plants.keys())
        category = all_categories[int(call_body)]
        all_plants = list(plants[category].keys())
        cur_plant = all_plants[int(attr)]
        add_user_plant(call.message.chat.id, f"{category}/{cur_plant}")
        markup = telebot.types.InlineKeyboardMarkup()
        cnt = 0
        for inf in plants[category][cur_plant].keys():
            #print(inf)
            if inf == 'name':
                cnt += 1
                continue
            btn = telebot.types.InlineKeyboardButton(text= inf, callback_data= f"2:{call_body}:{cnt}")
            markup.add(btn)
            cnt += 1
        my_plants = get_user_plants(user_id=call.message.chat.id)
        if not f"{category}/{cur_plant}" in my_plants:
            btn = telebot.types.InlineKeyboardButton(text= "Добавить к себе.", callback_data=f"6:{all_categories.index(category)}:{all_plants.index(cur_plant)}")
        else:
            btn = telebot.types.InlineKeyboardButton(text= "Удалить из моих.", callback_data=f"7:{all_categories.index(category)}:{all_plants.index(cur_plant)}")
        markup.add(btn)
        my = telebot.types.InlineKeyboardButton(text= "К моим растениям", callback_data=f'5:{call.message.chat.id}:{0}')
        markup.add(my)
        btn = telebot.types.InlineKeyboardButton(text= "↩️Назад к Категории↩️", callback_data=f"0:{category}:")
        markup.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Растение: {cur_plant}.", reply_markup=markup)
        return 

    if group == '7':
        all_categories = list(plants.keys())
        category = all_categories[int(call_body)]
        all_plants = list(plants[category].keys())
        cur_plant = all_plants[int(attr)]
        remove_user_plant(call.message.chat.id, f"{category}/{cur_plant}")
        markup = telebot.types.InlineKeyboardMarkup()
        cnt = 0
        for inf in plants[category][cur_plant].keys():
            #print(inf)
            if inf == 'name':
                cnt += 1
                continue
            btn = telebot.types.InlineKeyboardButton(text= inf, callback_data= f"2:{call_body}:{cnt}")
            markup.add(btn)
            cnt += 1
        my_plants = get_user_plants(user_id=call.message.chat.id)
        if not f"{category}/{cur_plant}" in my_plants:
            btn = telebot.types.InlineKeyboardButton(text= "Добавить к себе.", callback_data=f"6:{all_categories.index(category)}:{all_plants.index(cur_plant)}")
        else:
            btn = telebot.types.InlineKeyboardButton(text= "Удалить из моих.", callback_data=f"7:{all_categories.index(category)}:{all_plants.index(cur_plant)}")
        markup.add(btn)
        my = telebot.types.InlineKeyboardButton(text= "К моим растениям", callback_data=f'5:{call.message.chat.id}:{0}')
        markup.add(my)
        btn = telebot.types.InlineKeyboardButton(text= "↩️Назад к Категории↩️", callback_data=f"0:{category}:")
        markup.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Растение: {cur_plant}.", reply_markup=markup)
        return 
    # не опознаный колл (call) ботом
    # bot.send_message(chat_id=owner_id, text = f"404, Этот колл бот не смог обработать!\n\n{call.data}", parse_mode="html")



"""
def check_notification_date(user_id, notification_date):
    today = datetime.date.today()
    if today.day % notification_date == 0:
        message = "Привет! Сегодня тот день, когда нужно уведомить тебя!"
        print(message)


while True:
    with open("user_data.json", 'r', encoding='ascii') as json_file:
        user_data_dict = json.load(json_file)

        now = datetime.datetime.now()
        if now.hour == 13 and now.minute == 00:
            for user_id in user_data_dict:
                notification_date = user_data_dict[user_id]['f']
                check_notification_date(user_id, notification_date)
        # time.sleep(1)  # Ждем одну минуту перед следующей проверкой
"""

bot.polling(none_stop=True)