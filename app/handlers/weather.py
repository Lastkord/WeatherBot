from telegram import Update
from telegram.ext import ContextTypes
from statemacine import state_machine


async def weather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'city' not in context.user_data:
        return await state_machine.states[0](update, context)
    return await state_machine.states[1](update, context)
