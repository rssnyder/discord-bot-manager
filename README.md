# discord-bot-manager

an api to help you manage your other bots

## auth

lazy: using the browser dev tools, capture a post call and view the `Authorization` header

```shell
export AUTH='mfa_' # Authorization header
export TEAMS='["00000000000000"]' # json of team ids to create bots in
export DB='./bots' # optional
export DB_TABLE='bots' # optional
```

## main

fastapi server to enable bot creation via http

`uvicorn main:app`

## create_bot

create a new discord application

create a new discord bot and generate a token (these together are one action)

store the corresponding id and token in a database (totally optional)

run as a script if you happen to be remoted into the server

`./create_bot.py`
