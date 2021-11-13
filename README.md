# discord-bot-manager

an api to help you manage your other bots

## storage

postgres

```shell
export DB_HOST="" # postgres host
export DB_DB="" # postgres database
export DB_USER="" # postgres user
export DB_PASS="" # postgres password
```

## auth

lazy: using the browser dev tools, capture a post call and view the `Authorization` header

```shell
export AUTH='mfa_' # Authorization header
export TEAMS='["00000000000000"]' # json of team ids to create bots in
```

## main

fastapi server to enable bot creation via http

`uvicorn main:app`

## create_bot

create a new discord application

create a new discord bot and generate a token (these together are one action)

## db

store a new bot in the db

get a bot from the db

mark a bot as claimed

get count of unclimed bots
