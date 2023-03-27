from dotenv import load_dotenv
import urllib.parse
import requests
import telebot
import os

load_dotenv()

TOKEN = os.environ.get('TG_TOKEN')
API_URL = os.environ.get('API_URL')
GROUP_ID = os.environ.get('TG_GROUP_ID')

bot = telebot.TeleBot(TOKEN)

def get_posts():
    response = requests.get(f"{API_URL}/posts")
    if response.ok:
        return response.json()
    else:
        return None

def get_post(post_id):
    response = requests.get(f"{API_URL}/posts?id={post_id}")
    if response.ok:
        return response.json()
    else:
        return None

def make_caption(post):
    return f"*{post['name'].upper()}*\n\n🧔Created by: {post['author']}\n\n[🔗 Link to the codepen]({post['link']})\n\n❤ Pen popularity: {post['likes']} likes"

@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton('Suggest me posts')
        markup.add(button)
        bot.send_message(message.chat.id, 'Hi! Press the button to suggest some posts.', reply_markup=markup)
    except Exception as e:
      print('Some error on start', e)

@bot.message_handler(func=lambda message: message.text == 'Suggest me posts')
def suggest_posts(message):
    try:
        bot.send_message(message.chat.id, 'Wait please...')
        posts = get_posts()
        if not posts:
            bot.send_message(message.chat.id, 'There is no posts... Try one more time!')
            return
        for post in posts:
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton('Post it!', callback_data=post['link'])
            markup.add(button)
            caption = make_caption(post)
            bot.send_photo(chat_id=message.chat.id, photo=post['image'], caption=caption, reply_markup=markup, parse_mode='Markdown')
        bot.send_message(message.chat.id, 'Select any post.')
    except Exception as e:
        bot.send_message(message.chat.id, 'Something went wrong... Try again!')
        print('Some error on getting post', e)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        post = get_post(call.data)
        if not post:
            bot.answer_callback_query(callback_query_id=call.id, text="Post not found...")
            return
        if post:
            caption = make_caption(post)
            bot.send_photo(chat_id=GROUP_ID, photo=post['image'], caption=caption, parse_mode='Markdown')
            bot.answer_callback_query(callback_query_id=call.id, text="Post sent!")
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="Post not found :(")
    except Exception as e:
          print('Some error while posting', e)

bot.polling()
