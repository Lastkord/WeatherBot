from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
)
from enums import States


async def city_display(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Напишите ваш город",
        reply_markup=ReplyKeyboardRemove()
    )

    return States.city.value
