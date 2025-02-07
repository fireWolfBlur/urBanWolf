from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import getChat, getChatMember,getConversation,addConversation,send_media,addUser
import asyncio

async def send_a_message(chat_id: int,user_data: list,context: CallbackContext,message_thread_id=None):
    first_name = user_data[0]
    user_id = user_data[1]
    text = f'• ID: <code>{user_id}</code>\n• Nom: {first_name}\n#id{user_id}'
    c = str(chat_id)
    c = c[4:]
    key= [
        [InlineKeyboardButton('Conversation 📨',url=f'http://t.me/c/{c}/{user_data[2]}')],
        [InlineKeyboardButton('Lu ✅',callback_data='see_msg')]
    ]
    reply_markup = InlineKeyboardMarkup(key)
    await context.bot.send_message(chat_id=chat_id,text=text,parse_mode='HTML',reply_markup=reply_markup,message_thread_id=message_thread_id)


async def sendAsk(name: str,chat_id: int,user_id:int,message,context: CallbackContext) -> bool:
    chat = await getChat(chat_id,context)
    if  chat == None:
        return False
    if chat.type == "supergroup":
        me = await context.bot.get_me()
        is_admin = await getChatMember(me.id,chat_id,context)

        if is_admin.status == "administrator" or is_admin.status == "creator" and is_admin.can_manage_chat:
            in_conversation = getConversation(user_id)
            if in_conversation == False:
                conversation_id = await context.bot.create_forum_topic(chat_id=chat_id,name=name)
                await send_media(message,chat_id,context,message_thread_id=conversation_id.message_thread_id)
                print(conversation_id)
                if addConversation(conversation_id.message_thread_id,chat_id,user_id):
                    print('nouvelle conversation ajouter')
                    return True
                else:
                    print('une erreur est survenue')
                    return False
            user_data = [name,user_id,in_conversation[1]]
            await send_a_message(chat_id,user_data,context)
            await send_media(message,chat_id,context,message_thread_id=in_conversation[1])
            return True
        else:
            return False

async def ask(update: Update,context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    CHAT_ID = -1002440454858
    me = await context.bot.get_me()
    if user_id != me.id:
        message = update.message
        addUser(user_id,first_name)
        await asyncio.sleep(1)
        added = await sendAsk(first_name, CHAT_ID, user_id, message, context)
        if added:
            await update.message.reply_text("Conversation added")
        else:
            await update.message.reply_text("Conversation not added")

async def send_a_message_to_chat(update: Update,context: CallbackContext):
    # in_conversation = getConversation(user_id)
    message = update.message
    me = await context.bot.get_me()
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    message_thread_id = message.message_thread_id
    in_conversation = getConversation(user_id,message_thread_id=message_thread_id)
    if in_conversation == False:
        return
    chat_id = in_conversation[0]
    if chat_id != me.id:
        await send_media(message,chat_id,context)
    