# discord-bot-manager

a bot to help you manage your other bots

## auth

lazy: using the browser dev tools, capture a post call and view the `Authorization` header

```shell
export AUTH='<header: Authorization>'
export DST_DB_TABLE='newbots' # optional
export DST_DB='/home/riley/Documents/isengard/newbots' # optional
export TEAMS='["00000000000000"]' # optional
```

## main

fastapi server to enabling creating bots via http

`uvicorn main:app`

## create_bot

create a new discord application

create a new discord bot and generate a token

store the corresponding id and token in a database

`./create_bot.py`
