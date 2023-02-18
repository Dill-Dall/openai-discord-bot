"""
Module to handle stuff related to quiz
"""

import json
import random
import asyncio
import time

import discord
from discord.ext import commands

import util
import dotcoordinate

jsonFolder = "QuizPersistent"

with open(f'{jsonFolder}\quotequiz.json', "r") as file:
    QUOTELIST = json.load(file)

with open(f'{jsonFolder}\countries_info2.json', "r") as file:
    COUNTRYLIST = json.load(file)

with open(f'{jsonFolder}\score.json', "r") as file:
    SCORECARD = json.load(file)


def add_point(name):
    with open(f'{jsonFolder}\score.json', "w") as file:
        for player in SCORECARD:
            if player["name"] == name:
                player["score"] = str(int(player["score"]) + 1)
                json.dump(SCORECARD, file, indent=4)
                return
        new_player = {}
        print(name)
        new_player["name"] = name
        new_player["score"] = 1
        new_player["id"] = SCORECARD[len(SCORECARD)-1]["id"] + 1
        SCORECARD.append(new_player)
        json.dump(SCORECARD, file, indent=4)

async def getScore(ctx):
    response = "################SCORECARD##############################\n#\n#\n"
    leader = ""
    leader_score = 0
    for player in SCORECARD:
        response += f'#     {player["name"]}: {player["score"]}\n'
        if int(player["score"]) > leader_score:
            leader = player["name"]
            leader_score = int(player["score"])

    await ctx.send(util.sWrap(f'{response}#\n#\n#   Guild quiz master is {leader}! with {leader_score} points! Cheers!\n#'
                            + '\n########################################################', util.StringStyle.YELLOW))

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='quiz', help='Starts a quiz about quotes.')
    async def quiz_me(self, ctx):
        quote_object = random.choice(QUOTELIST)
        if quote_object["said_by"] != "":
            await ctx.send(util.sWrap(f'{ctx.author.name}: The quote: “{quote_object["quote"]}” (id: {quote_object["id"]})\nWas said by?', util.StringStyle.CYAN))
            try:
                reply = await self.bot.wait_for('message', check=util.check(ctx.author), timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(util.sWrap(f'You were too slow!\nBut, can you name the {quote_object["genre"]}?', util.StringStyle.DIFF))
            else:
                if util.testContent(reply.content, quote_object['said_by']):
                    add_point(ctx.author.name)
                    await ctx.send(util.sWrap(f'{reply.content} is correctomundo!\nIt was said in which {quote_object["genre"]}?', util.StringStyle.YELLOW))

                else: await ctx.send(util.sWrap(f'-{reply.content} is FAIL!\nBut, can you name the {quote_object["genre"]}?', util.StringStyle.DIFF))

        else:
            await ctx.send(util.sWrap(f'{ctx.author.name}: The quote: “{quote_object["quote"]}” (id: {quote_object["id"]})\nWas said in which {quote_object["genre"]}?', util.StringStyle.CYAN))

        try:
            reply = await self.bot.wait_for('message', check=util.check(ctx.author), timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(util.sWrap("You were too slow, try again!", util.StringStyle.DIFF))
        else:
            if util.testContent(reply.content, quote_object["where"]):
                add_point(ctx.author.name)
                await ctx.send(util.sWrap(reply.content+" is correctomundo!", util.StringStyle.YELLOW))
            else:
                await ctx.send(util.sWrap(f'-{reply.content} is FAIL!!!', util.StringStyle.DIFF))

        reply = await self.bot.wait_for('message', check=util.check(ctx.author), timeout=30)
        if reply.content == "answer".lower():
            q_npc_string = quote_object["said_by"]
            if q_npc_string != "":
                q_npc_string = f'was said by accepted[{q_npc_string}] and'
            await ctx.send(f'{quote_object["quote"]} {q_npc_string} is from the {quote_object["genre"]} accepted[{quote_object["where"]}]')

    @commands.command(name='addquiz', help='can create quizes. Insert four util.StringStyle for the  fields:quote, said_by, where, genre: example: !addquiz "A quote from a film" "The name of the actor" "the name of the  film" "genre"... \n'
                     + 'for multiple accepted answers you can write for said_by or where "dasBoot,das boot,das boots" These are then all accepted answers for the said_by field.')
    async def add_quiz(self, ctx, quote, said_by, where, genre):
        questions = {}
        questions["quote"] = quote
        questions["said_by"] = said_by
        questions["where"] = where
        questions["genre"] = genre
        questions["id"] = QUOTELIST[len(QUOTELIST) - 1]["id"] + 1
        await ctx.send(util.sWrap(f'{ctx.author.name}: You have inserted  The quote: “{questions["quote"]}”\n'
                                  + f'said by: [{questions["said_by"]}]\n'
                                  + f'from: [{questions["where"]}]\n'
                                  + f'genre: {questions["genre"]}\n'
                                  + f'Is this ok?'
                                  + f'Type "yes", any other response will cancel the request', util.StringStyle.CYAN))
        reply = await self.bot.wait_for('message', check=util.check(ctx.author), timeout=30)
        if reply.content.lower() == "yes":
            QUOTELIST.append(questions)
            with open(f'{jsonFolder}\quotequiz.json', "w") as file:
                json.dump(QUOTELIST, file, indent=4)
            await ctx.send(util.sWrap(f'Great! You have entered a new quizset with id = {questions["id"]}. Thank you {ctx.author.name}!', util.StringStyle.CYAN))

    @commands.command(name='delquiz', help='Delete quiz based on id')
    async def del_quiz(self, ctx, quiz_id):
        if ctx.author.name != "DillDall" and ctx.author.name != "Blodappelsin":
            await ctx.send(util.sWrap(f'{ctx.author.name}! You forget yourself, such actions are beyond you. You are not the great DillDall!', util.StringStyle.CYAN))
            return
        with open(f'{jsonFolder}\quotequiz.json', "w") as file:
            for quote in QUOTELIST:
                if quote["id"] == int(quiz_id):
                    QUOTELIST.remove(quote)
                    await ctx.send(util.sWrap(f'You sucessfully deleted the quote with id = {quiz_id}', util.StringStyle.CYAN))
                    json.dump(QUOTELIST, file, indent=4)
                    return
        await ctx.send(util.sWrap(f'-Quote with id = {quiz_id} not found in Quotelist', util.StringStyle.NONE))

    @commands.command(name='score', help='Show scoreboard over quiz competitors')
    async def score(self, ctx):
        await getScore(ctx)


    @commands.command(name='startquiz_comp', help='Starts a quiz competition about quotes.')
    async def startquiz_comp(self, ctx, variant = "quotes", voiced = False,  nr_questions = 10, timer = 10):
        ret = 1

        if(variant == "country"):
            ret = await countryquiz_comp(self, ctx, nr_questions, timer, voiced)
        else:
            ret = await quotequiz_comp(self, ctx, nr_questions, timer, voiced)
        
        if(ret == 1): await getScore(ctx)

    
    @commands.command()
    async def test_map(self, ctx):
        map_file = dotcoordinate.circle_in(50, 50)
        print(map_file)
        await embeded_loop(self, ctx,"Which country is at the red circle?", map_file, "ape")


    

async def countryquiz_comp(self, ctx, nr_questions, timer, voiced):
    for x in range(1, int(nr_questions)+1):
        content =""
        msg = ""

        country_object = random.choice(COUNTRYLIST)

        questions_list = list()

        if 'flag' in country_object:
            print("flaggu")
            questions_list.append('flag')
        if 'lat' in country_object:
            questions_list.append('map')
            print("map")
        if 'capital' in country_object:
            print("capital")
            questions_list.append('capital')
        
        content = ""
        answer = ""

        question = random.choice(questions_list)
        if(question == "capital"):
            answer = country_object['capital'][0]
            country_name = country_object['name']['common']
            content =f'Question: {x} What is the capital of: “{country_name}”\n'
            
        if(question == "flag"):
            flag_file = f'QuizPersistent/flags/{country_object["flag"]}'
            answer = country_object['name']['common']
            await embeded_loop(self, ctx,"Which country's flag is this?", flag_file, answer)
            content =f'Question: {x} Which country\'s flag is this?"\n'
        elif (question == "map"):
            answer = country_object['name']['common']
            map_file = dotcoordinate.circle_in(float(country_object['long']), float(country_object['lat']))
            await embeded_loop(self, ctx,"Which country is at the red circle?", map_file, answer)
            content =f'Question: {x} "Which country is at the red circle?"\n'
        if (await answer_loop(self, ctx, content, timer, answer) == 0): return 0

    return 1


async def answer_loop(self, ctx, content, timer, correct_answer):
    answer = False
    timeout = time.time() + timer
    msg = await ctx.send(util.sWrap(content +  "Timer: 10", util.StringStyle.DIFF))

    while(not answer):
        try:
            reply = await self.bot.wait_for('message', check=util.checkBot(ctx.author, self.bot), timeout=1)
            if(reply.content == "q"):
                msg = await ctx.send("Questions aborted")
                return 0
            answer = util.testContent(reply.content, correct_answer)
            
        except asyncio.TimeoutError:
            time_left = round(timeout-time.time())
            if time_left < 0: time_left = 0
            
            await msg.edit(content = util.sWrap(f'{content} Timer: {time_left}', util.StringStyle.CYAN))
            if time.time() > timeout:
                await ctx.send(util.sWrap(f'- You were too slow!\n The answer was {correct_answer}', util.StringStyle.DIFF))
                break

        if(answer):
            add_point(reply.author.name)
            await ctx.send(util.sWrap(reply.content+" is correctomundo!", util.StringStyle.YELLOW))
           
async def embeded_loop(self, ctx, text,file,answer):
    embed = discord.Embed()
    await ctx.send(embed=embed, file=discord.File(file))

async def quotequiz_comp(self, ctx, nr_questions = 2, timer = 10, variant = "quotes", voiced = False):
    for x in range(1, int(nr_questions)+1):
        content =""
        msg = ""

        quote_object = random.choice(QUOTELIST)
        if quote_object["said_by"] != "":
            content =f'Question: {x} The quote: “{quote_object["quote"]}” (id: {quote_object["id"]})\nWas said by?'
            msg = await ctx.send(util.sWrap(content +  "Timer: 10", util.StringStyle.DIFF))
        
            answer = False
            timeout = time.time() + timer
            while(not answer):
                try:
                    reply = await self.bot.wait_for('message', check=util.checkBot(ctx.author, self.bot), timeout=1)
                    if(reply.content == "q"):
                        break
                    answer = util.testContent(reply.content, quote_object['said_by'])
                except asyncio.TimeoutError:
                    time_left = round(timeout-time.time())
                    if time_left < 0: time_left = 0
                
                    await msg.edit(content = util.sWrap(f'{content} Timer: {time_left}', util.StringStyle.CYAN))
                    if time.time() > timeout:
                        await ctx.send(util.sWrap(f'- You were too slow!', util.StringStyle.DIFF))
                        time.sleep(2)
                        break 

            if(answer):
                add_point(ctx.author.name)
                await ctx.send(util.sWrap(reply.content+" is correctomundo!", util.StringStyle.YELLOW))
                time.sleep(2)
        
            content = f'The quote Was said in which {quote_object["genre"]}?'
            msg = await ctx.send(util.sWrap(content, util.StringStyle.CYAN))
        else:
            content = f'The quote: “{quote_object["quote"]}” (id: {quote_object["id"]})\nWas said in which {quote_object["genre"]}?'
            msg = await ctx.send(util.sWrap(content, util.StringStyle.CYAN))
        
        answer = False
        timeout = time.time() + timer
        while(not answer):
            try:             
                reply = await self.bot.wait_for('message', check=util.checkBot(ctx.author, self.bot), timeout=1)
                if(reply.content == "q"):
                        break
                answer = util.testContent(reply.content, quote_object['where'])
            except asyncio.TimeoutError:
                time_left = round(timeout-time.time())
                if time_left < 0: time_left = 0
                await msg.edit(content = util.sWrap(f'{content} Timer: {time_left}', util.StringStyle.CYAN))
            if time.time() > timeout:
                await ctx.send(util.sWrap(f'- You were too slow!', util.StringStyle.DIFF))
                break  

        if(answer):
            add_point(ctx.author.name)
            await ctx.send(util.sWrap(reply.content+" is correctomundo!", util.StringStyle.YELLOW))
            
        time.sleep(1)
        q_npc_string = quote_object["said_by"]
        if q_npc_string != "":
            q_npc_string = f'was said by accepted[{q_npc_string}] and'
        content = f'{quote_object["quote"]} {q_npc_string} is from the {quote_object["genre"]} accepted[{quote_object["where"]}]'                
        await ctx.send(util.sWrap(content, util.StringStyle.DIFF))