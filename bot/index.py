from dotenv import load_dotenv
import requests
import telebot
import os
import json

load_dotenv()

TOKEN = os.environ.get('TG_TOKEN')
API_URL = os.environ.get('API_URL')
GROUP_ID = os.environ.get('TG_GROUP_ID')

bot = telebot.TeleBot(TOKEN)

temp_posts = []

def mark_as_posted(id):
    response = requests.get(f"{API_URL}/posts/mark/{id}")
    if response.ok:
        return response.json()
    else:
        return None

def get_posts():
    response = requests.get(f"{API_URL}/posts")
    if response.ok:
        return response.json()
    else:
        return None


def parse_posts():
    response = requests.get(f"{API_URL}/parse")
    if response.ok:
        return response.json()
    else:
        return None


def save_post(post):
    response = requests.post(f"{API_URL}/posts", json=post)
    if response.ok:
        return response.json()
    else:
        return None

def get_posts_by_id(id):
    response = requests.get(f"{API_URL}/posts/{id}")
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
        parse_button = telebot.types.KeyboardButton('Parse new posts')
        get_from_db_button = telebot.types.KeyboardButton('Show saved posts')
        markup.add(parse_button, get_from_db_button)
        bot.send_message(message.chat.id, 'Hi! I\'m ready to work.', reply_markup=markup)
    except Exception as e:
        print('Some error on start', e)


@bot.message_handler(func=lambda message: message.text == 'Parse new posts')
def show_parsed_posts(message):
    try:
        bot.send_message(message.chat.id, 'Wait please...')
        posts = parse_posts()
        if not posts['data']:
            bot.send_message(message.chat.id, 'There is no posts... Parse it before!')
            return
        if posts['error']:
            bot.send_message(message.chat.id, posts['error'])
            return
        temp_posts.extend(posts['data'])
        for post in posts['data']:
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton('Save it!', callback_data=post['link'])
            markup.add(button)
            caption = make_caption(post)
            bot.send_photo(
                chat_id=message.chat.id,
                photo=post['image'],
                caption=caption,
                reply_markup=markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        bot.send_message(message.chat.id, 'Something went wrong... Try again!')
        print('Some error on parsing post', e)


@bot.message_handler(func=lambda message: message.text == 'Show saved posts')
def show_saved_posts(message):
    try:
        bot.send_message(message.chat.id, 'Wait please...')
        posts = get_posts()
        if not posts['data']:
            bot.send_message(message.chat.id, 'There is no posts... Try one more time!')
            return
        if posts['error']:
            bot.send_message(message.chat.id, posts['error'])
            return
        for post in posts['data']:
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton('Post it!', callback_data=post['id'])
            markup.add(button)
            caption = make_caption(post)
            bot.send_photo(
                chat_id=message.chat.id,
                photo=post['image'],
                caption=caption,
                reply_markup=markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        bot.send_message(message.chat.id, 'Something went wrong... Try again!')
        print('Some error on getting posts from db', e)

def save_parsed_post(call):
    try:
        post = None
        for _post in temp_posts:
            if _post['link'] == call.data:
                post = _post
        if not post:
            bot.answer_callback_query(callback_query_id=call.id, text="Post not found...")
            return
        if post:
            save_post(post)
            bot.answer_callback_query(callback_query_id=call.id, text="Post saved to db!")
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="Post not found :(")
    except Exception as e:
        print('Some error while posting', e)

def post_to_group(call):
    try:
        post = get_posts_by_id(call.data)
        if not post['data']:
            bot.answer_callback_query(callback_query_id=call.id, text="Post not found...")
            return
        if post['data']:
            caption = make_caption(post['data'])
            bot.send_photo(chat_id=GROUP_ID, photo=post['data']['image'], caption=caption, parse_mode='Markdown')
            bot.answer_callback_query(callback_query_id=call.id, text="Post sent to the group!")
            mark_as_posted(post['data']['id'])
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="Post not found :(")
    except Exception as e:
        print('Some error while posting', e)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith('http'):
        save_parsed_post(call)
    elif call.data.isnumeric():
        post_to_group(call)
    else:
        print('callback_query data -> ', call.data)




bot.polling()
