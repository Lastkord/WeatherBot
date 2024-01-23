from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from enums import States


async def weather_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [

        [InlineKeyboardButton("На один день", callback_data=1)],
        [InlineKeyboardButton("На два дня", callback_data=2)],
        [InlineKeyboardButton("На три дня", callback_data=3)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выберите на сколько дней хотите получить прогноз погоды:",
        reply_markup=reply_markup
    )
    return States.weather.value
