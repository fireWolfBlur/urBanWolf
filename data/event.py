import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from config import addEVent,getEvent,getUser
from datetime import datetime
from data.db import connector

CONFIRM_EVENT,TITLE,DESCRIPTION,MEDIA,DATE_START,DATE_END = range(6)

async def start_event(update: Update,context: CallbackContext) -> int:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    await update.message.reply_text('Entrez le titre de l\'événement')
    return TITLE

async def title(update: Update,context: CallbackContext) -> int:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    title = update.message.text
    context.user_data['title'] = title
    await update.message.reply_text('Entrez la description de l\'événement')
    return DESCRIPTION

async def description(update: Update,context: CallbackContext) -> int:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    description = update.message.text
    context.user_data['description'] = description
    await update.message.reply_text('Entrez le media de l\'événement')
    return MEDIA

async def media(update: Update,context: CallbackContext) -> int:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    media = update.message
    if media.photo:
        media = media.photo[-1].file_id if media.photo else None
        context.user_data['media'] = media
    else:
        media = None
        context.user_data['media'] = media
    await update.message.reply_text("Quelle est la date de début ? (Format: YYYY-MM-DD HH:MM)")
    return DATE_START

async def date_start(update: Update,context: CallbackContext) -> int:
    try:
        context.user_data['date_start'] = datetime.strptime(update.message.text, "%Y-%m-%d %H:%M")
        await update.message.reply_text("Quelle est la date de fin ? (Format: YYYY-MM-DD HH:MM)")
        return DATE_END
    except ValueError:
        await update.message.reply_text("Format invalide. Essaie à nouveau (YYYY-MM-DD HH:MM).")
        return DATE_START

async def date_end(update: Update,context: CallbackContext) -> int:
    try:
        user = update.message.from_user
        user_id = user.id
        context.user_data['date_end'] = datetime.strptime(update.message.text, "%Y-%m-%d %H:%M")
        context.user_data['user_id'] = user_id

        conn, cursor = connector()
        cursor.execute("select max(event_id) from events")
        current_id = cursor.fetchone()
        if current_id[0] is None:
            current_id = 1
        else:
            current_id = current_id[0] + 1
        context.user_data['current_id'] = current_id

        keyboard = [
            [
                InlineKeyboardButton('Valider ✅',callback_data='confirm_event=yes'),
                InlineKeyboardButton('Refuser ❌',callback_data='confirm_event=no')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Voulez vous vraiment ajouter cette évenement ?",reply_markup=reply_markup)

        return CONFIRM_EVENT
    except ValueError:
        await update.message.reply_text("Format invalide. Essaie à nouveau (YYYY-MM-DD HH:MM).")
        return DATE_END

async def get_event(update: Update,context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text("Entrez l'ID de l'événement")
        return
    event_id = context.args[0]
    try:
        event_id = int(event_id)
    except ValueError:
        await update.message.reply_text("ID invalide")
        return
    event = getEvent(event_id)
    if event:
        title,description,media,date_start,date_end,add_by = event
        user = getUser(add_by)
        first_name = user
        mention = f'<a href="tg://user?id={add_by}">{first_name}</a>'
        text = f"<b>#event 🎉:</b> <i>{title}</i>\n<b>📍Description:</b> \n\n<i>{description}</i>\n\n<b>🗓️ Date de début:</b> <i>{date_start}</i>\n\n<b>🗓️ Date de fin:</b> <i>{date_end}</i>\n<b>👤 Ajouté par:</b> <i>{mention}</i>"
        if media is not None:
            await update.message.reply_photo(photo=media,caption=text,parse_mode='HTML')
        else:
            await update.message.reply_text(text,parse_mode='HTML')

    else:
        await update.message.reply_text("Aucun événement trouvé")