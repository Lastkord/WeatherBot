import httpx
from config import WEATHER_TOKEN
from telegram import Update
from telegram.ext import ContextTypes


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
    context.user_data['weather_type'] = update.message.text
    index = 0
    match context.user_data['weather_type']:
        case 'На один день':
            index = 1
        case 'На два дня':
            index = 2
        case 'На три дня':
            index = 3
    result = httpx.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_TOKEN}&q={context.user_data['city']}&days={index}").json()
    weather = get_response_to_few_days(result)
    for item in weather:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            caption=item['text'],
            photo=item['img']
        )
    return 1
