import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

bot=telebot.TeleBot('6145801037:AAFbHpVEw7sQcJExgwTu4Vn0CJDGyvOQWdE')

def get_prise(url):
    res=requests.get(url)
    soup=BeautifulSoup(res.text, "lxml")
    data=soup.find('div', class_="sc-f70bb44c-0 flfGQp flexStart alignBaseline")
    k=str(data)
    l=k.find('$')
    k=k[l:]
    g=k.find('<')
    k=k[:g]
    return k
def get_coincapitalization(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    data = soup.find('dd', class_='sc-f70bb44c-0 bCgkcs base-text')
    k = str(data)
    l = k.find('$')
    k = k[l:]
    l = k.find('<')
    k = k[:l]
    return k


@bot.message_handler(content_types=['photo','video','audio'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton('Delete message', callback_data='delete')
    markup.row(btn1)
    bot.send_message(message.chat.id, 'Sorry, but I don\'t know how to work with the file.',reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data=='delete':
        try:
            bot.delete_message(callback.message.chat.id,callback.message.message_id-1)
        except BaseException:
                pass



@bot.message_handler(commands=['menu'])
def menu(message):
    markup2 = types.ReplyKeyboardMarkup()
    btn8 = types.InlineKeyboardButton('xrp')
    btn9 = types.InlineKeyboardButton('shiba')
    btn10 = types.InlineKeyboardButton('bone')
    btn11 = types.InlineKeyboardButton('leash')
    btn12 = types.InlineKeyboardButton('help')
    btn13 = types.InlineKeyboardButton('info')
    markup2.row(btn8, btn9, btn10, btn11)
    markup2.row(btn12, btn13)
    bot.send_message(message.chat.id, 'Select the navigation item you need', reply_markup=markup2)



@bot.message_handler(commands=['message'])
def printk(message):
    bot.send_message(message.chat.id,message)

@bot.message_handler(commands=['start'])
def start(message):
    markup1=types.ReplyKeyboardMarkup()
    btn2=types.KeyboardButton('xrp')
    btn3 = types.KeyboardButton('shiba')
    btn4 = types.KeyboardButton('bone')
    btn5 = types.KeyboardButton('leash')
    btn6 = types.KeyboardButton('help')
    btn7 = types.KeyboardButton('info')
    markup1.row(btn2,btn5,btn3,btn4)
    markup1.row(btn7,btn6)
    usernname1=message.from_user.username
    if message.from_user.language_code == 'ru':
        if usernname1 == None:
            usernname1 = 'Пользователь'
            bot.send_message(message.chat.id,f'Привет,{usernname1}!',reply_markup=markup1)
    else:
        if usernname1 == None:
            usernname1 = 'User'
            bot.send_message(message.chat.id, f'Hello,{usernname1}!',reply_markup=markup1)



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,'Бла бла бла' )

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,'Для связи обращаться сюда: barselona2k18@mail.ru' )


@bot.message_handler(commands=['shiba'])
def shib(message):
    bot.send_message(message.chat.id,'Shib\n'+'Price:'+' '+get_prise('https://coinmarketcap.com/currencies/shiba-inu/') \
                     +'\nCoin capitalization:'\
                     +get_coincapitalization('https://coinmarketcap.com/currencies/shiba-inu/'))

@bot.message_handler(commands=['bone'])
def bone(message):
    bot.send_message(message.chat.id,'Bone\n'+'Price:'+''+get_prise('https://coinmarketcap.com/currencies/bone-shibaswap/')\
                     +'\nCoin capitalization:'\
                     +get_coincapitalization('https://coinmarketcap.com/currencies/bone-shibaswap/') )


@bot.message_handler(commands=['leash'])
def leash(message):
    bot.send_message(message.chat.id,'leash\n'+'Price:'+' '+get_prise('https://coinmarketcap.com/currencies/doge-killer/') \
                     +'\nCoin capitalization:'\
                     +get_coincapitalization('https://coinmarketcap.com/currencies/doge-killer/'))

@bot.message_handler(commands=['xrp'])
def xrp(message):
    bot.send_message(message.chat.id,'xrp\n'+'Price:'+''+get_prise('https://coinmarketcap.com/currencies/xrp/')\
                     +'\nCoin capitalization:'\
                     +get_coincapitalization('https://coinmarketcap.com/currencies/xrp/'))


@bot.message_handler()
def sent(message):
    if message.text.lower() == 'shiba':
        try:
         bot.send_message(message.chat.id,shib(message))
        except BaseException:
            pass
    elif message.text.lower() == 'bone':
        try:
         bot.send_message(message.chat.id,bone(message))
        except BaseException:
            pass
    elif message.text.lower() == 'leash':
        try:
         bot.send_message(message.chat.id,leash(message))
        except BaseException:
            pass
    elif message.text.lower() == 'xrp':
        try:
         bot.send_message(message.chat.id,xrp(message))
        except BaseException:
            pass

bot.polling(none_stop=True)
