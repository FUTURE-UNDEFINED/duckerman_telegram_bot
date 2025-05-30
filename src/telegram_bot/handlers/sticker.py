import asyncio
import io
import uuid

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Sticker
from telegram.ext import CallbackContext, MessageHandler, filters, CallbackQueryHandler

from telegram_bot.grpc_client import tg_stick_conv_client
from generated.telegram_stickers_converter.telegram_stickers_converter_pb2 import GetStickerRequest, OutputFormat

from cachetools import TTLCache


class SessionContext:
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update


sessions = TTLCache(maxsize=1000, ttl=300)


def create_animated_stickers_keyboard(sticker: Sticker, session_id: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("PNG", callback_data=f"png:{session_id}"),
            # InlineKeyboardButton("JPG", callback_data=f"jpg:{session_id}"),
            InlineKeyboardButton("WEBP", callback_data=f"webp:{session_id}"),
        ],
        [
            # InlineKeyboardButton("WEBM", callback_data=f"webm:{session_id}"),
            # InlineKeyboardButton("MP4", callback_data=f"mp4:{session_id}"),
            # InlineKeyboardButton("GIF", callback_data=f"gif:{session_id}"),
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)
    return markup


def create_video_stickers_keyboard(sticker: Sticker, session_id: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            # InlineKeyboardButton("MP4", callback_data=f"mp4:{session_id}"),
            # InlineKeyboardButton("MPEG", callback_data=f"MPEG:{session_id}"),
            InlineKeyboardButton("GIF", callback_data=f"gif:{session_id}"),
        ],
        [
            InlineKeyboardButton("WEBM", callback_data=f"webm:{session_id}"),
            # InlineKeyboardButton("MOV", callback_data=f"mov:{session_id}"),
            # InlineKeyboardButton("WEBP", callback_data=f"webp:{session_id}"),
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)
    return markup


def create_static_stickers_keyboard(sticker: Sticker, session_id: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("WEBP", callback_data=f"webp:{session_id}"),
            InlineKeyboardButton("PNG", callback_data=f"png:{session_id}"),
            # InlineKeyboardButton("JPG", callback_data=f"jpg:{session_id}"),
        ],
    ]

    markup = InlineKeyboardMarkup(keyboard)
    return markup


def save_sticker_session(user_id: int, sticker: Sticker) -> str:
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {
        "user_id": user_id,
        "sticker_file_id": sticker.file_id,
        "is_animated": sticker.is_animated,
        "is_video": sticker.is_video,
        "stage": "format_selection",
        "chosen_format": None,
    }

    return session_id


async def handle_sticker(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    sticker = update.message.sticker

    print(sticker)

    session_id = save_sticker_session(user_id, sticker)

    markup = None
    if update.message.sticker.is_animated:
        markup = create_animated_stickers_keyboard(update.message.sticker, session_id)
    elif update.message.sticker.is_video:
        markup = create_video_stickers_keyboard(update.message.sticker, session_id)
    else:
        markup = create_static_stickers_keyboard(update.message.sticker, session_id)

    await context.bot.send_message(update.effective_chat.id, "Select desired format", reply_markup=markup)


sticker_handler = MessageHandler(filters=filters.Sticker.ALL, callback=handle_sticker)


def format_to_output(format: str) -> OutputFormat:
    formats = {
        "png": OutputFormat.OUTPUT_FORMAT_PNG,
        "webp": OutputFormat.OUTPUT_FORMAT_WEBP_ANIMATED,
        "webm": OutputFormat.OUTPUT_FORMAT_WEBM,
        "mp4": OutputFormat.OUTPUT_FORMAT_MP4,
        "gif": OutputFormat.OUTPUT_FORMAT_GIF,
        "jpg": OutputFormat.OUTPUT_FORMAT_JPG,
    }

    return formats[format]

async def send_resolution_keyboard(update: Update, context: CallbackContext, session_id: str):
    keyboard = [
        [InlineKeyboardButton("1K", callback_data=f"1k:{session_id}"),
         InlineKeyboardButton("2K", callback_data=f"2k:{session_id}")],
        [InlineKeyboardButton("4K", callback_data=f"4k:{session_id}"),
         InlineKeyboardButton("8K", callback_data=f"8k:{session_id}")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выбери разрешение:", reply_markup=markup)


async def send_final_sticker(update: Update, context: CallbackContext, session_data: dict, width: int, height: int):
    req = GetStickerRequest(
        sticker_file_id=session_data["sticker_file_id"],
        desired_format=format_to_output(session_data["chosen_format"]),
        is_animated=session_data["is_animated"],
        is_video=session_data["is_video"],
        width=width,
        height=height,
    )

    chunks = []
    try:
        async for resp in tg_stick_conv_client.GetSticker(req):
            if resp.HasField("data_chunk"):
                chunks.append(resp.data_chunk)
            elif resp.HasField("metadata"):
                print(f"Received metadata: {resp.metadata}")
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ошибка: {e}")
        return

    file_bytes = b"".join(chunks)
    file_stream = io.BytesIO(file_bytes)
    file_stream.name = f"sticker.{session_data['sticker_file_id']}.{session_data['chosen_format']}"

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=file_stream,
        caption="Вот твой стикер!",
    )


async def handle_sticker_cb_query(update: Update, context: CallbackContext):
    data = update.callback_query.data
    await context.bot.answer_callback_query(update.callback_query.id)

    parts = data.split(":")
    action = parts[0].lower()
    session_id = parts[1]
    session_data = sessions[session_id]

    if session_data["stage"] == "format_selection":
        session_data["chosen_format"] = action

        if session_data["is_animated"]:
            session_data["stage"] = "resolution_selection"

            await context.bot.delete_message(update.effective_chat.id, update.callback_query.message.message_id)
            await send_resolution_keyboard(update, context, session_id)
            return
        else:
            await context.bot.delete_message(update.effective_chat.id, update.callback_query.message.message_id)
            await send_final_sticker(update, context, session_data, 1024, 1024)
            return

    elif session_data["stage"] == "resolution_selection":
        resolution = action
        size = 1024
        if resolution == '1k':
            size = 1024
        elif resolution == '2k':
            size = 2048
        elif resolution == '4k':
            size = 4096
        elif resolution == '8k':
            size = 8196
        print(size)
        try:
            await context.bot.delete_message(update.effective_chat.id, update.callback_query.message.message_id)
            await context.bot.send_message(update.effective_chat.id, "Processing sticker, please wait...")
            asyncio.create_task(send_final_sticker(update, context, session_data, size, size))
        except Exception as e:
            print(e)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Internal bot error...")
        return

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Internal bot error...")


sticker_cb_query_handler = CallbackQueryHandler(callback=handle_sticker_cb_query)
