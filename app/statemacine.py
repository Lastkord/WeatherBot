from displays.city import city_display
from displays.weather import weather_display
from telegram import Update
from telegram.ext import ContextTypes


class StateMachine(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(StateMachine, cls).__new__(cls)
        return cls.instance

    states = {
        0: city_display,
        1: weather_display
    }

    async def move(
        self, state: int, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        return await self.states[state](update, context)


state_machine = StateMachine()