from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from telegram_bot.bot import bot_app
from telegram_bot.handlers.sticker import sticker_handler, sticker_cb_query_handler


async def handle_start_command(update: Update, context: CallbackContext):
    msg_text = "Привет! Отправь стикер который нужно обработать."
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id,
                                       text=msg_text)
    except Exception as e:
        print("Failed to send message:", e)


start_cmd_handler = CommandHandler(command="start", callback=handle_start_command)

def main():
    bot_app.add_handler(sticker_handler)
    bot_app.add_handler(sticker_cb_query_handler)
    bot_app.add_handler(start_cmd_handler)
    bot_app.run_polling()
