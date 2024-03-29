from telegram import Update
from telegram.ext import ContextTypes
from statemacine import state_machine
from enums import States


async def city_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text(text=f"Ваш город {context.user_data['city']}")
    return await state_machine.states[States.weather.value](update, context)
