# quiz_bot.py
# implement main bot fuctionality

import os
import asyncio
import discord

# from db_utils import db_utils
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)
# dbu = db_utils()

# discord async get input after command
# takes a specified prompt and timeout, returns reply (or times out)
async def get_input(ctx, message, timeout=5):
    await ctx.send(message)

    # condition check for receiving message
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout) # 30 seconds to reply
        return msg.content
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return 0

# on ready is called when the bot logs in
# BUG: this function gives diagnostic error 
#   "guild is possibly unbound?"
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.command()
async def WhoAmI(ctx):
    """Returns username, id, potentially list of classes"""
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


@bot.command()
async def SetupUser(ctx, *args):
    """Set up user in database and add classes to their record if added"""
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


@bot.command()
async def RemoveClasses(ctx, *args):
    """Provide user with means remove classes from sched"""
    return


@bot.command()
async def AddClasses(ctx, *args):
    """Add classes to db"""
    if len(args) == 0:
        err_msg = (f'Command requires class name with list of topics, i.e. !AddClassTopic cpsc231 java oo polymorphism')
        await ctx.send(err_msg)
    else:
        test_msg = ""
        for class_name in args:
            test_msg += f'class name: {class_name}\n'
        await ctx.send(test_msg)

    dbu.add_class_topic(args[0], args[1:len(args)])
    return


@bot.command()
async def AddQuestion(ctx, class_name="none"):
    """gets a class as arg, prompts for question to enter"""
    #TODO: figure out how to extract topic
    if class_name == "none":
        await ctx.send("Command requires class name --> ex. '!AddQuestion relational algebra'")
    else:
        msg = await get_input(ctx, "what's the question?")

    if msg != 0:
        await ctx.send(f'you said {msg}')


#TODO: implement answer question


#TODO: implement get question
async def GetQuestion(ctx, class_name="none"):
    """return question based on user class"""
    # check if it's a class or a topic
    # if its nothing then get question from any other the user's classes


#TODO: implement get answers


#TODO: implement get all classes
    

#TODO: implement get all topics



bot.run(TOKEN)
