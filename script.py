from sqlalchemy import create_engine, MetaData



string = 'postgresql://bot:password@localhost:5432/bot_db'

engine = create_engine(string)
connect = engine.connect()