FROM python:3.10

WORKDIR /usr/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk update \
#    && apk add gcc python3 py-pip libffi-dev py3-cffi \
#    && pip install --upgrade pip \

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN apt-get -y update
RUN apt-get -y upgrade
# RUN pip3 install --upgrade pip

COPY ./poetry.lock ./pyproject.toml /usr/app/
RUN poetry install

COPY . /usr/app/

#RUN ls
# CMD ["python3", "$EXECUTE_PATH"]