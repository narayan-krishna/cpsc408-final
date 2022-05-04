# quiz_bot.py
# implement main bot fuctionality

import os
import asyncio
import discord

# from db_utils import db_utils
from discord.ext import commands
from dotenv import load_dotenv

from db_utils import db_utils


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)
dbu = db_utils()


# discord async get input after command
# takes a specified prompt and timeout, returns reply (or times out)
# RETURNS 0 ON FAILURE
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


#parse bot message for tag
def parse_msg(mystr):
    if mystr[0] == '[':
        print("has a tag")
        tag = mystr.split(']')[0]
        id = tag[1]
        type = tag[2:]
        return type, id
    else:
        return -1, -1


# on ready is called when the bot logs in
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


#TODO: NEEDS TESTING
# track emojis on questions
@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)

    # check whether the message with the emoji is a bot message
    if message.author.id == bot.user.id:
        if payload.emoji.name == '👍':
            type, table_id = parse_msg(message.content)
            if type == 'A':
                # do something wtih type, table_id
                # increment_likes(table_id)
                print('A')
            msg = "a bot message received a like"
            await channel.send(msg)


@bot.command()
async def WhoAmI(ctx):
    """Returns username, id, potentially list of classes"""
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )

    # TODO: query print user classes
    await ctx.send(msg)


@bot.command()
async def SetupUser(ctx):
    """Set up user in database and add classes to their record if added"""
    userID = str(ctx.message.author.id)
    userName = str(ctx.message.author.name)
    
    #print("\n\n\nDEBUG: "+userID + userName +"\n\n\n")
    dbu.add_user(userID,userName)
    msg = "You've been added to the database!\n"
    await ctx.send(msg)


#TODO: begin implement
@bot.command()
async def RemoveClasses(ctx, *args):
    """Provide user with means remove classes from sched"""
    return


@bot.command()
async def AddClass(ctx, *args):
    """Add classes to db"""
    if len(args) == 1:
        dbu.add_class(ctx.message.author.id,args[0])
        #err_msg = (f'Command requires class name with list of topics, i.e. !AddClassTopic cpsc231 java oo polymorphism')
        #await ctx.send(err_msg)
        return
    else:
        err_msg = (f'Command only takes one argument as input, the name of the class.')
        await ctx.send(err_msg)


@bot.command()
async def AddQuestion(ctx, class_name="none"):
    """gets a class as arg, prompts for question to enter"""
    #TODO: figure out how to extract topic
    if class_name == "none":
        await ctx.send("Command requires class name --> ex. '!AddQuestion relational algebra'")
    else:
        msg = await get_input(ctx, "what's the question?",30)
        dbu.add_question(ctx.message.author.id,msg)

    if msg != 0:
        await ctx.send(f'you said {msg}')


#TODO: implement answer question (NEEDS TESTING)
async def AnswerQuestion(ctx, question_id="none"):
    if question_id == "none":
        await ctx.send("Command requires a question id --> ex. '!AnswerQuestion 1101'")
    else:
        msg = await get_input(ctx, "what's your answer to the question?",30)
        dbu.answer_question(ctx.message.author.id,question_id,msg)


#TODO: implement get question
@bot.command()
async def GetQuestion(ctx):
    """return question based on user class"""
    # if its nothing then get question from any other the user's classes
    await ctx.send(dbu.get_question(ctx.message.author.id))


#TODO: implement get all answers for a question (HMMMM)
@bot.command()
async def GetAnswers(ctx, question_id="none"):
    """get answers for a specific topic"""
    if question_id == "none":
        await ctx.send("Command requires a question id --> ex. '!AnswerQuestion 1101'")
    else:
        # TODO: implement dbutils funciton to to return all answers
        # msg = dbu.??()
        # await ctx.send(msg)
        return


# #TODO: implement get all classes
# @bot.command()
# async def GetClasses(ctx):
#     """return a list of classes"""
#     # get all classes from dbu.something
#     return


bot.run(TOKEN)
