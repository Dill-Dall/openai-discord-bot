from AiModels import AiModel
import os
import random
import string

import discord
import openai

import discord
import logging

discord.utils.setup_logging()


openai.api_key = os.getenv("OPENAI_API_KEY")
beer_number = os.getenv("BEER_NUMBER")
admin_user = os.getenv("ADMIN_USER")
dev_channel = os.getenv("DEV_CHANNEL")

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


def doOpenAiQuestion(prompt, temperature=0.5, max_tokens=150, top_p=0.3, frequency_penalty=0.5,
                     presence_penalty=0.0):

    logging.info("PROMPT: {}".format(prompt))
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            # TODO: prompt should be able to take multiple values. Perhaps prompt as a parameter?  Because propmpt  cant have multiple variables like this.
            prompt=prompt,
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


def generate_prompt(AiModel, inputs):
    formatted_inputs = [input.capitalize() for input in inputs]
    return AiModel.value.format(*formatted_inputs)


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
    return generate_prompt(AiModel.GLADOS, [str(int(weighted_random(10, 100, 30))), ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVW", k=random.randint(10, 30)))])


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(int(dev_channel))
    await channel.send(doOpenAiQuestion(glados_prompt()))


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
    elif message.content.startswith('Timmy'):
        question = message.content.replace('Timmy', '')
        prompt = generate_prompt(AiModel.TIMMY, question)
        response = doOpenAiQuestion(prompt)
        await message.channel.send(response)
    elif message.content.startswith('Glados'):
        response = doOpenAiQuestion(glados_prompt())
        await message.channel.send(response)
    elif message.content.startswith('Glen'):
        question = message.content.replace('Glen', '')
        prompt = generate_prompt(AiModel.GLEN, question)
        response = doOpenAiQuestion(prompt, temperature=0.3, max_tokens=int(weighted_random(12, 24, 6)), presence_penalty=0.2,
                                    frequency_penalty=0.3)
        await message.channel.send(response)


client.run(os.getenv("DISCORD_TOKEN"))
