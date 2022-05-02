# quiz_bot.py
# implement main bot fuctionality

import os
import asyncio
import discord

from db_utils import db_utils
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
dbu = db_utils()


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


@bot.command(pass_context = True)
async def whoami(ctx):
    """Returns username, id, potentially list of classes"""
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


@bot.command(pass_context = True)
async def SetUpUser(ctx):
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


@bot.command()
async def AddClass(ctx, class_name="none"):
    """Add class to classes table given name"""
    if class_name == "none":
        return
    dbu.add_class(class_name)
    await ctx.send(f'topic added: {class_name}')


@bot.command()
async def AddClassTopic(ctx, *args):
    """Add class topics given specified class"""
    if len(args) == 0:
        err_msg = (
            f'Command requires class name with list of topics, i.e. !AddClassTopic cpsc231 java oo polymorphism'
        )
        await ctx.send(err_msg)
    else:
        test_msg = ""
        for index,arg in enumerate(args):
            if index == 0:
                test_msg += f'class name: {arg}\n'
            else:
                test_msg += f'class topic: {arg}\n'
        await ctx.send(test_msg)
    return


@bot.command()
async def AddTopic(ctx, topic_name="none"):
    if topic_name == "none":
        return
    dbu.add_topic(topic_name) 
    return


@bot.command()
async def AddQuestion(ctx, topic_name="none"):
    #TODO: figure out how to extract topic
    return


#TODO: implement answer question


#TODO: implement get question


#TODO: implement get answers
    
# discord async get input after command
# takes a specified prompt and timeout, returns reply (or times out)
async def get_input(ctx, message, timeout=5):
    await ctx.send(message)

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout) # 30 seconds to reply
        return msg.content
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return 0


bot.run(TOKEN)
