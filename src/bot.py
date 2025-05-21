import os

from telegram.ext import ApplicationBuilder

token = os.environ.get('TELEGRAM_TOKEN')
print(token)
bot_app = ApplicationBuilder().token(token).build()
