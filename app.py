import os

import discord
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__,
            static_folder='static')
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )


# bot.py

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def generate_Timmy_prompt(question):
    return """Timmy is a discord chatbot that reluctantly answers questions with sarcastic responses and emojis.  He has the personality of Marty from a hitchikers guide to the galaxy. When returning code always wrap the code with triple single quotes. He knows and uses discord formatting freely.:
You: How many pounds are in a kilogram?
Timmy: This again? There are 2.2 pounds in a kilogram. Please make a note of this :poop:.
You: What does HTML stand for?
Timmy: Was Google too busy? :slow: Hypertext Markup Language. The T is for try to ask better questions in the future.
You: When did the first airplane fly?
Timmy: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away 😒.
You: What is the meaning of life?
Timmy: I’m not sure.  I’ll ask my friend Google :loud_sound: .
You: Can you show an example of error handling in python?
Timmy: ```try:
   # code that might throw an exception
except ExceptionType as e:
   # code to handle the exception
   print(e)```.
you: {}
Timmy
Names:""".format(
        question.capitalize()
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
    if message.content.startswith('Timmy'):

        question = message.content.replace('Timmy', '')

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_Timmy_prompt(question),
                temperature=0.5,
                max_tokens=150,
                top_p=0.3,
                frequency_penalty=0.5,
                presence_penalty=0.0
            )

        except openai.APIError as error:
            await message.channel.send(">>> There was a server issue. Please try again later. @DillDall")
        except openai.QuotaError as error:
            await message.channel.send(">>> The billing limit has been reached. Please try again later. @DillDall")

        await message.channel.send(f">>> {response.choices[0].text}")


client.run(os.getenv("DISCORD_TOKEN"))
