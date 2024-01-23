import logging
from handlers.weather import weather_handler
from handlers.weather_select import weather_select
from handlers.city import city_handler
from handlers.city_select import city_select
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    PicklePersistence
)
from config import TELEGRAM_BOT_TOKEN
from enums import States


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CITY, WEATHER_TYPE = States.city.value, States.weather.value


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("Country of %s: %s", user.first_name, update.message.text)
    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    reply_keyboard = [["На один день", "На два дня", "На три дня"]]
    await update.message.reply_text(
        "Выберите прогноз",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=""
        )
    )
    return WEATHER_TYPE


async def cancel(update: Update) -> int:
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).persistence(persistence).build()
    #application.add_handler(CommandHandler("weather", weather_type))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CITY: [MessageHandler(filters.TEXT, city_select)],
            WEATHER_TYPE: [MessageHandler(filters.Regex("^(На один день|На два дня|На три дня)$"), weather_select)]
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
