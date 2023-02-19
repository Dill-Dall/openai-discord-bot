import os
import random

import discord
from discord.ext import commands
import logging

from AiModels import AiModel
from open_ai_query import do_openai_question, do_openai_image_create
from prompt_helpers import generate_prompt, get_random_theme, weighted_random

logging.basicConfig(level=logging.INFO)


dev_channel = os.getenv("DEV_CHANNEL")

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():

    def generate_glados_prompt():
        theme = get_random_theme()

        wordlength = random.randint(10, 100)

        return generate_prompt(AiModel.GLADOS, [theme, str(wordlength-10), str(wordlength+10)])

    logging.info(f"We have logged in as {bot.user}")
    embed = discord.Embed(title='Booting...', color=discord.Color.blue())
    channel = bot.get_channel(int(dev_channel))

    working_message = await channel.send(embed=embed)
    response = do_openai_question(generate_glados_prompt(), temperature=1)

    embed = discord.Embed(
        title='Glados', description=response, color=discord.Color.blue())
    await working_message.edit(embed=embed)


@bot.slash_command(name="timmy", description="Timmy helps you, but might be dificult about it")
async def timmy_command(ctx, *, question):
    await ctx.defer()
    prompt = generate_prompt(AiModel.TIMMY, question)
    response = do_openai_question(prompt)

    embed = discord.Embed(color=discord.Color.blue())
    embed.add_field(name=ctx.author.name, value=question, inline=False)
    embed.add_field(name='Timmy', value=response)

    await ctx.followup.send(embed=embed)


@bot.slash_command(name="glados", description="Say quotes and comments on them. #Struggling with random")
async def glados_command(ctx):
    await ctx.defer()
    response = do_openai_question(generate_glados_prompt(), temperature=1)
    embed = discord.Embed(
        title='Glados', description=response, color=discord.Color.blue())

    await ctx.followup.send(embed=embed)


# Would be great if one could create multiple seperated messages but think threads must be  used
@bot.slash_command(name="convo", description="Creates a new thread, where you can have a continous conversation")
async def frendo_command(ctx):
    response = await ctx.respond('Starting conversation...', allowed_mentions=discord.AllowedMentions(users=False))
    message = await ctx.send('What can I help you with?')
    thread = await message.create_thread(name='convo-conversation-', auto_archive_duration=10080)
    if isinstance(response, discord.Interaction):
        await response.delete_original_response()


@bot.event
async def on_message(message: discord.Message):
    thread = message.channel
    if isinstance(thread, discord.Thread) and thread.owner == bot.user:
        if message.author == bot.user:
            return

        if message.content.strip().lower() == "delete":
            await thread.delete()
            return

        await bot.process_commands(message)
        async with message.channel.typing():
            bigPrompt = generate_prompt(AiModel.CONVO, '') + '\n'
            messages = await thread.history(limit=None).flatten()
            messages.reverse()
            for message in messages:
                if message.author == bot.user:
                    bigPrompt += 'AI:' + message.content.strip() + '\n'
                else:
                    bigPrompt += 'Human:' + message.content.strip() + '\n'

            logging.info('PROMPT:\n'+bigPrompt)

            await thread.send(do_openai_question(bigPrompt))

            if len(messages) % 10 == 0:
                title = do_openai_question(
                    "Give a title for this thread:" + bigPrompt, max_tokens=20)
                logging.info(title)
                await thread.edit(name=title)


@bot.slash_command(name="glen", description="Responds with short and concise answers")
async def glen_command(ctx, *, question):
    await ctx.defer()
    response = do_openai_question(
        prompt=generate_prompt(AiModel.GLEN, question),
        temperature=0.3,
        max_tokens=int(weighted_random(12, 24, 6)),
        presence_penalty=0.2,
        frequency_penalty=0.3
    )
    embed = discord.Embed(color=discord.Color.blue())
    embed.add_field(name=ctx.author.name, value=question, inline=False)
    embed.add_field(name='Glen', value=response)
    await ctx.followup.send(embed=embed)


@bot.slash_command(name="dall", description="Uses the Dalle engine to create images by prompt")
async def dall_command(ctx, *, prompt):
    await ctx.defer()
    response = do_openai_image_create(prompt)
    image_url = response['data'][0]['url']

    embed = discord.Embed(title='Dall',
                          color=discord.Color.blue())
    embed.add_field(name=ctx.author.name, value=prompt)
    embed.set_image(url=image_url)

    await ctx.followup.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
