import bs4
import requests as r
import telebot
import urllib.request as urllib2
import os
from telebot import apihelper

apihelper.proxy = {'https': 'socks5://sox.ctf.su:1080'}
bot = telebot.TeleBot("759430792:AAHsG4FbJRdjz7NikDhXS6wIT7mP1SqfhKc")
print(bot.get_me())


def log(message):
    from datetime import datetime
    print("\n----")
    print(datetime.now())
    print("Message from {0} {1}: (id = {2})\n{3}".format(message.from_user.first_name,
                                                         message.from_user.last_name,
                                                         str(message.from_user.id),
                                                         message.text))


# books with a pic only
def bookList(message, url):
    bot.send_message(message.from_user.id, 'Подождите немного')

    data = r.get(url)
    soup = bs4.BeautifulSoup(data.text, "html.parser")

    books = soup.select('tr b a')
    pics = []
    tempPics = soup.select('img')

    for i in tempPics:
        if i['src'].split('?')[0] == 'https://spblib.ru:443/catalog':
            pics.append(i['src'])
    counter = 0
    for i in range(len(books)):
        urllib2.urlretrieve(pics[i], 'image.jpg')
        if os.stat('image.jpg').st_size != 0:
            with open('image.jpg', 'rb') as img:
                # first words before point. the names are big as fuck
                bot.send_chat_action(message.from_user.id, 'upload_photo')
                bot.send_photo(message.from_user.id, img, caption=books[i].text.split('.')[0] + "\n" + books[i]['href'])
                counter += 1
    if counter != 0:
        bot.send_message(message.from_user.id, 'Больше ничего не нашел:с')
    else:
        bot.send_message(message.from_user.id, 'Вообще ничего не нашел:с')
        bot.send_message(message.from_user.id, 'Но подожди!!! Сейчас...')
        bot.send_message(message.from_user.id, 'http://g.zeos.in/?q=' + message.text)


def joke():
    z = ''
    s = r.get('http://anekdotme.ru/random')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.anekdot_text')
    for x in p:
        s = (x.getText().strip())
        z = z + s + '\n\n'
    return s


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start')
    user_markup.row('Список книг')
    bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=user_markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    log(message)
    if u'анекдот' in message.text.lower():
        bot.send_message(message.from_user.id, joke())
    elif message.text == 'Список книг':
        bookList(message, 'https://spblib.ru/catalog')

    elif message.text != '':
        bookList(message, 'https://spblib.ru/catalog/-/books/search/' + message.text + '#search-results')


bot.polling(none_stop=True, interval=0)
