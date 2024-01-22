from telegram import Update
from telegram.ext import ContextTypes
from statemacine import state_machine


async def city_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await state_machine.states[0](update, context)
