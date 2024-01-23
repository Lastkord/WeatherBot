from telegram import Update
from telegram.ext import ContextTypes
from statemacine import state_machine
from enums import States


async def city_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await state_machine.states[States.city.value](update, context)
