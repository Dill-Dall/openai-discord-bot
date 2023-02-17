from AiModels import AiModel
import os
import random
import requests
from io import BytesIO

import discord
import openai

import logging

openai.api_key = os.getenv("OPENAI_API_KEY")
beer_number = os.getenv("BEER_NUMBER")
admin_user = os.getenv("ADMIN_USER")
dev_channel = os.getenv("DEV_CHANNEL")

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


def do_openai_question(prompt, temperature=0.5, max_tokens=150, top_p=0.3, frequency_penalty=0.5,
                       presence_penalty=0.0):

    logging.info("PROMPT: {}".format(prompt))
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

    except openai.APIError as error:
        if error.status_code == 429:
            return f"The billing limit has been reached. Please try again later. Else you can :beer: me @{admin_user} at {beer_number}"
        return f"There was a server issue. Please try again later. @{admin_user}"

    return f"{response.choices[0].text.lstrip()}"


def generate_prompt(ai_model, inputs):
    if isinstance(inputs, str):
        inputs = [inputs]
    formatted_inputs = [input.capitalize() for input in inputs]
    return ai_model.value.format(*formatted_inputs)


def weighted_random(lowest, highest, std_dev):
    mean = (lowest + highest) / 2
    iteration = 0
    while iteration < 1500:
        num = random.normalvariate(mean, std_dev)
        if lowest <= num <= highest:
            return num
        iteration += 1
    return mean


def glados_prompt():
    wordlength = random.randint(10, 100)
    return generate_prompt(AiModel.GLADOS, [str(wordlength-10), str(wordlength+10)])


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))
    embed = discord.Embed(title='Booting...', color=discord.Color.blue())
    channel = client.get_channel(int(dev_channel))
    working_message = await channel.send(embed=embed)
    response = do_openai_question(glados_prompt())

    embed.title = "Glados"
    await embed_complete(embed, working_message, response)


async def embed_complete(embed, working_message, response):
    embed.color = discord.Color.green()
    embed.description = response
    await working_message.edit(embed=embed)


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if any(message.content.startswith(prefix) for prefix in ['Timmy', 'Glados', 'Glen', 'Dall']):
        embed = discord.Embed(title='Working...', color=discord.Color.blue())
        working_message = await message.channel.send(embed=embed)

        if message.content.startswith('Timmy'):
            question = message.content.replace('Timmy', '')
            prompt = generate_prompt(AiModel.TIMMY, question)
            response = do_openai_question(prompt)
            embed.title = 'Timmy'

        elif message.content.startswith('Glados'):
            response = do_openai_question(glados_prompt())
            embed.title = 'Glados'

        elif message.content.startswith('Glen'):
            question = message.content.replace('Glen', '')
            prompt = generate_prompt(AiModel.GLEN, question)
            response = do_openai_question(
                prompt,
                temperature=0.3,
                max_tokens=int(weighted_random(12, 24, 6)),
                presence_penalty=0.2,
                frequency_penalty=0.3
            )
            embed.title = 'Glen'

        elif message.content.startswith('Dall'):
            embed.set_image(
                url='https://media.giphy.com/media/dtHz6tzJp3fbmopSwA/giphy.gif')
            await working_message.edit(embed=embed)

            prompt = message.content.replace('Dall', '')
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            image_url = response['data'][0]['url']
            response = requests.get(image_url)
            # image_data = BytesIO(response.content)

            embed.set_image(url=image_url)
            response = prompt
            embed.title = 'Dall'

    await embed_complete(embed, working_message, response)

client.run(os.getenv("DISCORD_TOKEN"))
