import logging
import httpx
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN, WEATHER_TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

COUNTRY, CITY, WEATHER_TYPE = range(3)


def get_response_to_few_days(data):
    result = []
    for day in data['forecast']['forecastday']:
        for hour in day['hour']:
            precip = "Не ожидаются" if hour['precip_mm'] < 10 else "Ожидаются"
            cloud = "Облачно" if hour['cloud'] > 60 else "Ясно"
            text = (f'Погода на {hour["time"]}.\n'
                  f'Температура: {hour["temp_c"]}°С.\n'
                  f'Ощущается как {round(hour["feelslike_c"])}.\n'
                  f'Осадки: {precip}.\n'
                  f'Ветер: {hour["wind_mph"]} м/с.\n'
                  f'{cloud}')
            result.append({"text": text, "img": hour["condition"]["icon"][2:]})
    return result


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Беларусь", "Россия", "Украина"]]

    await update.message.reply_text(
        "<Выберите вашу страну>?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="Country?",
            resize_keyboard=True
        ),
    )
    return COUNTRY


async def country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    context.user_data["country"] = update.message.text
    logger.info("Country of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Напишите ваш город",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    context.user_data["city"] = update.message.text
    logger.info(f"{user.first_name} Country: {context.user_data['country']} City: {context.user_data['city']}")
    reply_keyboard = [["На один день", "На два дня", "На три дня"]]
    await update.message.reply_text(
        "Выберите прогноз",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="А??????????????????7"
        )
    )
    return WEATHER_TYPE


async def weather_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['weather_type'] = update.message.text
    match context.user_data['weather_type']:
        case 'На один день':
            result = httpx.get(
                f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={context.user_data['city']}&days=1").json()
            weather = get_response_to_few_days(result)
            for item in weather:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    caption=item['text'],
                    photo=item['img']
                )

        case 'На два дня':
            result = httpx.get(
                f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={context.user_data['city']}&days=2").json()
            weather = get_response_to_few_days(result)
            for item in weather:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    caption=item['text'],
                    photo=item['img']
                )
        case 'На три дня':
            result = httpx.get(
                f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={context.user_data['city']}&days=3").json()
            weather = get_response_to_few_days(result)
            for item in weather:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    caption=item['text'],
                    photo=item['img']
                )



async def cancel(update: Update) -> int:
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            COUNTRY: [MessageHandler(filters.Regex("^(Беларусь|Россия|Украина)$"), country)],
            CITY: [MessageHandler(filters.TEXT, city)],
            WEATHER_TYPE: [MessageHandler(filters.Regex("^(На один день|На два дня|На три дня)$"), weather_type)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
