FROM python:3.11

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT uvicorn --host 0.0.0.0 --port 7777 main:app
