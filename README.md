OpenAI Discord Bot
==================

The `openai-discord-bot` project is a Python-based Discord bot that uses OpenAI's API to generate natural language responses and images in response to user commands.

Getting started
---------------

To use the `openai-discord-bot` project, you will need to:

1.  Clone the repository to your local machine.
2.  Install the required Python packages using `pip install -r requirements.txt`.
3.  Set up the necessary environment variables in a `.env` file in the root directory of the project. The required environment variables are:

*   `DISCORD_TOKEN`: Your Discord bot token. -> [discord developer](https://discordapp.com/developers/applications)
*   `OPENAI_API_KEY`: Your OpenAI API key. -> [openai.com/api](https://openai.com/api/)

4.  Start the bot by running `python discord_bot.py`.

Docker usage
------------

To run the app on a server:


```bash
#Install Docker 	
cp .env.example .env 	
#Then input the required values into the .env keys 	
docker run --env-file .env --rm --name discord-openai-bot thomda/openai-discord-bot:latest
```

Usage
-----

The `openai-discord-bot` project provides several slash commands that trigger different OpenAI models to generate responses to user queries:

*   `/glados`: Generates a quote or comment from the GLaDOS AI model.
*   `/timmy`: Generates a response to a user's question using the TIMMY AI model.
*   `/glen`: Generates a short and concise answer to a user's question using the GLEN AI model.
*   `/dall`: Generates an image from the DALL-E AI model using the specified prompt.

To use the bot, simply type one of these commands in a Discord channel where the bot is present, followed by any additional required parameters.

Contributing
------------

If you want to contribute to the `openai-discord-bot` project, feel free to fork the repository and submit a pull request with your changes. All kinds of contributions are welcome, including bug fixes, new features, and improvements to the existing code.

Refferences
-----------

*   [pycord](https://docs.pycord.dev)
*   [openai.com/api](https://openai.com/api/)
