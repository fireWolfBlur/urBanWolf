from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from config import addEVent, send_media
async def buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    if data == 'see_msg':
        await query.delete_message()
    if data.startswith('confirm_event'):
        action = data.split("=")[1]

        title = context.user_data['title']
        description = context.user_data['description']
        media = context.user_data['media']
        date_start = context.user_data['date_start']
        date_end = context.user_data['date_end']
        current_id = context.user_data['current_id']
        add_by = context.user_data['user_id']

        CHAT_ID = -1002440454858

        if action == 'yes':
            keyboard = [
            [
                InlineKeyboardButton('Valider ✅',callback_data=f'confirm_add_event?{current_id}=yes'),
                InlineKeyboardButton('Refuser ❌',callback_data=f'confirm_add_event?{current_id}=no')
            ]
        ]
            await query.edit_message_text(
                "Merci d'avoir ajouter cette évenement *Veillez attendre la confirmation de l'evenement par nos administrateur* 🗳",
                parse_mode='MarkdownV2'
            )
            if media is None:
                await context.bot.send_message(
                    text=f"📅 <b>{title}\n\n{description}\n\n📅 Date de début: {date_start}\n📅 Date de fin: {date_end}\n\nvalider vous cette evenement ?</b>",
                    chat_id=CHAT_ID,
                    parse_mode='HTML',
                    message_thread_id=221,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await context.bot.send_photo(
                caption = f"📅 <b>{title}\n\n{description}\n\n📅 Date de début: {date_start}\n📅 Date de fin: {date_end}\n\nvalider vous cette evenement ?</b>",
                photo= media,
                chat_id=CHAT_ID,
                parse_mode='HTML',
                message_thread_id=221,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.edit_message_text("Annulé")
            return ConversationHandler.END
    
    if data.startswith('confirm_add_event'):
        action = data.split("=")[1]
        event_id = data.split("?")[1]

        title = context.user_data['title']
        description = context.user_data['description']
        media = context.user_data['media']
        date_start = context.user_data['date_start']
        date_end = context.user_data['date_end']
        current_id = context.user_data['current_id']
        add_by = context.user_data['user_id']

        if action == 'yes':
            await query.edit_message_reply_markup(None)
            await update.message.reply_text("L'évenement a été ajouter avec succès ✅")
            addEVent(event_id, title, description, media, date_start, date_end, add_by)
            await context.bot.send_message(text=f"L'évenement a été ajouter avec succès ✅\n ID de l'évenement: {current_id}",chat_id=add_by)
        else:
            await query.edit_message_reply_markup(None)
            await update.message.reply_text("L'évenement a été refuser ❌")
            await context.bot.send_message(text=f"L'évenement a été refuser ❌",chat_id=add_by)


