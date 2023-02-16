import os
import random
import string

import discord
import openai

from AiModels import AiModel

openai.api_key = os.getenv("OPENAI_API_KEY")
beer_number = os.getenv("BEER_NUMBER")
admin_user = os.getenv("ADMIN_USER")
dev_channel = os.getenv("DEV_CHANNEL")

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


def doOpenAiQuestion(AiModel, question, temperature=0.5, max_tokens=150, top_p=0.3, frequency_penalty=0.5,
                     presence_penalty=0.0):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(AiModel, question),
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

    except openai.APIError as error:
        return f">>> There was a server issue. Please try again later. @{admin_user}"
    except openai.InvalidRequestError as error:
        return f">>> The billing limit has been reached. Please try again later. Else you can :beer: me @{admin_user} at {beer_number}"

    return f">>> {response.choices[0].text.lstrip()}"


def generate_prompt(AiModel, question):
    return AiModel.value.format(
        question.capitalize()
    )


def weighted_random(lowest, highest, std_dev):
    mean = (lowest + highest) / 2
    iteration = 0
    while iteration < 1500:
        num = random.normalvariate(mean, std_dev)
        if lowest <= num <= highest:
            return num
        iteration += 1
    return mean


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    random_string = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=random.randint(10, 50)))
    channel = client.get_channel(dev_channel)
    await channel.send(doOpenAiQuestion(AiModel.GLADOS, random_string, 2))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
    elif message.content.startswith('Timmy'):
        question = message.content.replace('Timmy', '')
        response = doOpenAiQuestion(AiModel.TIMMY, question)
        await message.channel.send(response)
    elif message.content.startswith('Glen'):
        question = message.content.replace('Glen', '')
        response = doOpenAiQuestion(AiModel.GLEN, question, temperature=0.3, max_tokens=int(weighted_random(12, 24, 6)), presence_penalty=0.2,
                                    frequency_penalty=0.3)
        await message.channel.send(response)


client.run(os.getenv("DISCORD_TOKEN"))
