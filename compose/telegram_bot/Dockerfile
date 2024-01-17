FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /telegram_bot
WORKDIR /telegram_bot

COPY requirements.txt /telegram_bot
RUN pip install --no-cache-dir -r requirements.txt

COPY /app /telegram_bot/app


CMD ["python", "app/main.py"]