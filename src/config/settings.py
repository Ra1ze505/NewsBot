import os

try:
    from dotenv import load_dotenv
    load_dotenv('../.env')
    load_dotenv('../../../.env')
    load_dotenv('../../.env')
    load_dotenv('./.env')
except:
    pass


# Bot settings
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
STRING_SESSION = os.environ.get('STRING_SESSION')
ADMIN_TG_ID = int(os.environ.get('ADMIN_TG_ID'))

# Database
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

# News chanel
NEWS_CHANEL = os.environ.get('NEWS_CHANEL')
KEY_WORD = os.environ.get('KEY_WORD')

# Weather
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=6&appid={token}&units=metric&lang=ru'
WEATHER_API_NOW_URL = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&lang=ru&units=metric'

# Currency rates
CURRENCY_API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')