from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)


async def weather_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["На один день", "На два дня", "На три дня"]]
    await update.message.reply_text(
        "Выберите прогноз",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=""
        )
    )
    return 1
