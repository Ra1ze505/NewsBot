import os


# Bot settings
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
STRING_SESSION = os.environ.get('STRING_SESSION')

# Database
DB_DRIVER = os.environ.get('DB_DRIVER', 'sqlite')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME', 'database.db')

# News chanel
NEWS_CHANEL = os.environ.get('NEWS_CHANEL')
KEY_WORD = os.environ.get('KEY_WORD')