import httpx
from config import WEATHER_TOKEN
from telegram import Update
from telegram.ext import ContextTypes
from enums import States
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


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


async def weather_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    result = httpx.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={context.user_data['city']}&days={query.data}").json()
    weather = get_response_to_few_days(result)
    for item in weather:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            caption=item['text'],
            photo=item['img']
        )
    return States.weather.value
