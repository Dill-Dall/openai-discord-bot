# open-discord-bot - Python discor app querying openai.
Open ai Discord bot, based on the https://beta.openai.com/docs/quickstart

## Setup
Prerequisites:
1: api key from openai : https://openai.com/api/
2: discord bot token from discord: https://discordapp.com/developers/applications

Install:
1: Install docker

2: Make a copy of the example environment variables file and input the corresponding values

```$ cp .env.example .env```

3: Run
```$ docker pull thomda/openai-discord-bot:latest && docker run --env-file .env --rm --name discord-openai-bot thomda/openai-discord-bot:latest```
