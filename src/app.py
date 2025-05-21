import sys
import os

current_script_dir = os.path.dirname(os.path.abspath(__file__))
generated_dir_path = os.path.join(current_script_dir, "generated")
if generated_dir_path not in sys.path:
    sys.path.insert(0, generated_dir_path)

from bot import bot_app
from handlers.sticker import sticker_handler, sticker_cb_query_handler

if __name__ == '__main__':
    bot_app.add_handler(sticker_handler)
    bot_app.add_handler(sticker_cb_query_handler)
    bot_app.run_polling()
