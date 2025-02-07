from telegram import Update
from telegram.ext import CallbackContext
from data.db import connector
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
async def getChat(chat_id: int,context):
    # This function is used to get the chat object from the chat_id
    # This is useful for checking if the chat exists

    in_chat = await context.bot.get_chat(chat_id)
    return in_chat

async def getChatMember(user_id,chat_id: int,context):
    # This function is used to get the chat object from the chat_id
    # This is useful for checking if the chat exists

    in_chat = await context.bot.get_chat_member(chat_id,user_id)
    return in_chat

def getConversation(user_id: int,message_thread_id=None):
    conn, cursor = connector()
    res = None
    if message_thread_id is None:
        cursor.execute('select user_id,message_thread_id from conversations where user_id=?',(user_id,))
        res = cursor.fetchone()
    else:
        cursor.execute('select user_id from conversations where message_thread_id=?',(message_thread_id,))
        res = cursor.fetchone()
    if res == None:
        conn.close()
        return False
    conn.close()
    return res
    
def getUser(user_id: int):
    conn, cursor = connector()
    cursor.execute('select first_name,in_proced from users where user_id=?',(user_id,))
    res = cursor.fetchone()
    if res == None:
        conn.close()
        return False
    conn.close()
    return res[0]

def addConversation(message_thread_id: int,chat_id: int,user_id:int) -> bool:
    conn, cursor = connector()

    cursor.execute('select user_id from conversations where user_id=?',(user_id,))
    res = cursor.fetchone()
    print(res)
    if res is None:
        cursor.execute("insert into conversations(user_id,chat_id,message_thread_id) values(?,?,?)",(user_id,chat_id,message_thread_id))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def addUser(user_id: int,first_name: str) -> bool:
    conn, cursor = connector()
    cursor.execute('select user_id from users where user_id=?', (user_id,))
    res = cursor.fetchone()
    if res is None:
        cursor.execute("insert into users(user_id, first_name) values(?, ?)", (user_id, first_name))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def addEVent(event_id: int,title: str,description: str,media: str,date_start: str,date_end: str,add_by: int) -> bool:
    conn, cursor = connector()
    cursor.execute('select event_id from events where event_id=?', (event_id,))
    res = cursor.fetchone()
    if res is None:
        cursor.execute("insert into events(event_id, title, description, media, date_start, date_end, add_by) values(?, ?, ?, ?, ?, ?, ?)", (event_id, title, description, media, date_start, date_end, add_by))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def getEvent(event_id: int):
    conn, cursor = connector()
    cursor.execute('select title, description, media, date_start, date_end, add_by from events where event_id=?', (event_id,))
    res = cursor.fetchone()
    if res is None:
        conn.close()
        return False
    conn.close()
    return res

def deleteEvent(event_id: int) -> bool:
    conn, cursor = connector()
    cursor.execute('delete from events where event_id=?', (event_id,))
    conn.commit()
    conn.close()

async def send_media(message, chat_id, context: CallbackContext, message_thread_id=None, parse_mode=None, reply_markup=None, disable_notification=False):
    if message.text:
        await context.bot.send_message(chat_id=chat_id, text=message.text, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.photo:
        await context.bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id, caption=message.caption, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.video:
        await context.bot.send_video(chat_id=chat_id, video=message.video.file_id, caption=message.caption, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.document:
        await context.bot.send_document(chat_id=chat_id, document=message.document.file_id, caption=message.caption, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.audio:
        await context.bot.send_audio(chat_id=chat_id, audio=message.audio.file_id, caption=message.caption, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.voice:
        await context.bot.send_voice(chat_id=chat_id, voice=message.voice.file_id, caption=message.caption, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.sticker:
        await context.bot.send_sticker(chat_id=chat_id, sticker=message.sticker.file_id, message_thread_id=message_thread_id, disable_notification=disable_notification)
    elif message.animation:
        await context.bot.send_animation(chat_id=chat_id, animation=message.animation.file_id, caption=message.caption, message_thread_id=message_thread_id, parse_mode=parse_mode, reply_markup=reply_markup, disable_notification=disable_notification)
    elif message.video_note:
        await context.bot.send_video_note(chat_id=chat_id, video_note=message.video_note.file_id, message_thread_id=message_thread_id, disable_notification=disable_notification)
    elif message.location:
        await context.bot.send_location(chat_id=chat_id, latitude=message.location.latitude, longitude=message.location.longitude, message_thread_id=message_thread_id, disable_notification=disable_notification)
    elif message.venue:
        await context.bot.send_venue(chat_id=chat_id, latitude=message.venue.location.latitude, longitude=message.venue.location.longitude, title=message.venue.title, address=message.venue.address, message_thread_id=message_thread_id, disable_notification=disable_notification)
    elif message.contact:
        await context.bot.send_contact(chat_id=chat_id, phone_number=message.contact.phone_number, first_name=message.contact.first_name, last_name=message.contact.last_name, vcard=message.contact.vcard, message_thread_id=message_thread_id, disable_notification=disable_notification)

def alls():
    conn, cursor = connector()
    cursor.execute('select user_id from users')
    res = cursor.fetchall()
    print(res)
# alls()