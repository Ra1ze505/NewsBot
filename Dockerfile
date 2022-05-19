FROM python:3.10

WORKDIR /usr/src/app

COPY main/requirements.txt ./
COPY ./poetry.lock ./pyproject.toml /usr/src/app/
RUN pip install poetry==1.0.0
RUN  poetry install --no-dev --no-root

COPY . .

CMD [ "python", "./src/app/bot.py" ]