from logger import logger
from handlers.weather import weather_handler
from handlers.weather_select import weather_select
from handlers.city import city_handler
from handlers.city_select import city_select
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    PicklePersistence, CallbackQueryHandler
)
from config import TELEGRAM_BOT_TOKEN
from enums import States


CITY, WEATHER_TYPE = States.city.value, States.weather.value


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("Country of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(text=f"{user.first_name}! Добро пожаловать в Weather Bot. Если пользуешься мной впервые то скорее вводи команду /city и пиши город, где хочешь узнать погоду!")
    return CITY


async def cancel(update: Update) -> int:
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).persistence(persistence).build()
    application.bot.set_my_commands(
        commands=[
            BotCommand("city", "Ввод города"),
            BotCommand("weather", "Прогноз погоды")
        ]
    )
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CITY: [MessageHandler(filters.TEXT, city_select)],
            WEATHER_TYPE: [CallbackQueryHandler(weather_select)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    menu_handlers = {
        'city': city_handler,
        'weather': weather_handler
    }
    for state in conv_handler.states:
        for command, handler in menu_handlers.items():
            conv_handler.states[state].insert(0, CommandHandler(command, handler))
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
