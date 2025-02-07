from config import TOKEN
from data import db
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext,CallbackQueryHandler

from data.covers import ask,send_a_message_to_chat

from data.callback import buttons

from data.event import start_event,title,description,media,date_start,date_end,get_event
from data.event import TITLE,DESCRIPTION,MEDIA,DATE_START,DATE_END,CONFIRM_EVENT

from telegram.ext import ConversationHandler

async def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_id = user.id
    first_name = user.first_name
    await update.message.reply_text('Annulé')
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_event', start_event)],
        states={
            TITLE: [MessageHandler(filters.ChatType.PRIVATE, title)],
            DESCRIPTION: [MessageHandler(filters.ChatType.PRIVATE, description)],
            MEDIA: [MessageHandler(filters.ChatType.PRIVATE, media)],
            DATE_START: [MessageHandler(filters.ChatType.PRIVATE, date_start)],
            DATE_END: [MessageHandler(filters.ChatType.PRIVATE, date_end)],
            CONFIRM_EVENT: [CallbackQueryHandler(buttons)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(CommandHandler('get_event', get_event))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE, ask))
    app.add_handler(MessageHandler(filters.ChatType.SUPERGROUP, send_a_message_to_chat))
    app.add_handler(CallbackQueryHandler(buttons))
    
    print('Bot is running!')
    app.run_polling()



if __name__ == '__main__':
    main()
