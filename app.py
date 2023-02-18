from AiModels import AiModel
import os
import random

import discord
import logging

from open_ai_query import do_openai_question, do_openai_image_create

dev_channel = os.getenv("DEV_CHANNEL")

bot = discord.Bot()


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


@bot.event
async def on_ready():
    logging.info(f"We have logged in as {bot.user}")
    embed = discord.Embed(title='Booting...', color=discord.Color.blue())
    channel = bot.get_channel(int(dev_channel))

    working_message = await channel.send(embed=embed)
    response = do_openai_question(glados_prompt())

    embed = discord.Embed(
        title='Glados', description=response, color=discord.Color.blue())
    await channel.send(embed=embed)


@bot.slash_command(name="timmy", description="Timmy helps you, but might be dificult about it")
async def timmy_command(ctx, *, question):
    async with ctx.typing():
        prompt = generate_prompt(AiModel.TIMMY, question)
        response = do_openai_question(prompt)
        embed = discord.Embed(
            title='Timmy', description=response, color=discord.Color.blue())
        await ctx.send(embed=embed)


@bot.slash_command(name="glados", description="Say quotes and comments on them. #Struggling with random")
async def glados_command(ctx):
    response = do_openai_question(glados_prompt())
    embed = discord.Embed(
        title='Glados', description=response, color=discord.Color.blue())
    await ctx.send(embed=embed)


@bot.slash_command(name="glen", description="Responds with short and concise answers")
async def glen_command(ctx, *, question):
    response = do_openai_question(
        prompt=generate_prompt(AiModel.GLEN, question),
        temperature=0.3,
        max_tokens=int(weighted_random(12, 24, 6)),
        presence_penalty=0.2,
        frequency_penalty=0.3
    )
    embed = discord.Embed(
        title='Glen', description=response, color=discord.Color.blue())
    await ctx.respond(embed=embed)


@bot.slash_command(name="dall", description="Uses the Dalle engine to create images by prompt")
async def dall_command(ctx, *, prompt):
    await ctx.defer()
    response = do_openai_image_create(prompt)
    image_url = response['data'][0]['url']

    embed = discord.Embed(title='Dall', description=prompt,
                          color=discord.Color.blue())
    embed.set_image(url=image_url)

    await ctx.followup.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
