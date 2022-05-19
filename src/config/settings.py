import os


try:
    from dotenv import load_dotenv
    load_dotenv('./.env')
except Exception as e:
    pass

# Bot settings
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')

# Database
DB_DRIVER = os.environ.get('DB_DRIVER', 'sqlite')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME', 'database.db')