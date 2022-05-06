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


#TODO: this should be done?
#BUG: Doesn't look at total number of reacts
# Should use https://stackoverflow.com/questions/64842656/how-can-i-count-the-number-of-reactions-in-discord-js instead
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
            # print("\n\n\n"+str(type)+"\n\n\n")
            #print("\n\n\n"+str(table_id)+"\n\n\n")
            if table_id == 'A':
                dbu.increment_likes(type)
                # print('A')
            msg = "a bot message received a like"
            await channel.send(msg)


@bot.command()
async def WhoAmI(ctx):
    """Returns username, id, and list of classes"""
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )

    await ctx.send(msg)
    # TODO: query print user classes
    await ctx.send("[UNIMPLEMENTED]: Classes: ")


@bot.command()
#TODO: Should this be on Login instead of when the user types it?
async def SetupUser(ctx):
    """Sets you up in our database"""
    userID = str(ctx.message.author.id)
    userName = str(ctx.message.author.name)
    
    #TODO: Don't add to database if userID exists -- test success check
    success = dbu.add_user(userID,userName)
    if success == 1:
        msg = "You've been added to the database!\n"
        await ctx.send(msg)
    else:
        msg = "You're id exists within databse\n"
        await ctx.send(msg)


#TODO: begin implement
@bot.command()
async def RemoveClass(ctx, classToRemove = None):
    """Remove the class specified by [classToRemove]"""
    if classToRemove == None:
        await ctx.send("Usage: !RemoveClass [classToRemove]")
        return
    await ctx.send("[UNIMPLEMENTED]: Removing class {}".format(classToRemove))


@bot.command()
async def AddClass(ctx, classToAdd = None, *args):
    """Add [classToAdd] to classes in database"""

    if len(args) == 0 and classToAdd != None:
        dbu.add_class(ctx.message.author.id, classToAdd)
        #err_msg = (f'Command requires class name with list of topics, i.e. !AddClassTopic cpsc231 java oo polymorphism')
        #await ctx.send(err_msg)
        return
    else:
        err_msg = (f'Usage: !AddClass [classToAdd]')
        await ctx.send(err_msg)

@bot.command()
async def UpdateAnswer(ctx, *args):
    """Add [classToAdd] to classes in database"""

    if len(args) != 2:
        err_msg = (f'Command requires two arguments [AnswerID,NewAnswerText]')
        await ctx.send(err_msg)
        return
    else:
            if args[0].isnumeric() and args[1].isnumeric() != True:
                dbu.update_answer(ctx.message.author.id,args[0],args[1])
                await ctx.send(err_msg)


@bot.command()
async def DropClass(ctx, classToDrop = None, *args):
    """Drops User from Class"""
    if len(args) == 0 and classToDrop != None:
        dbu.drop_class(ctx.message.author.id, classToDrop)
        #err_msg = (f'Command requires class name with list of topics, i.e. !AddClassTopic cpsc231 java oo polymorphism')
        #await ctx.send(err_msg)
        msg = (f'Class Dropped.')
        await ctx.send(msg)
    else:
        err_msg = (f'Usage: !DropClass [classToDrop]')
        await ctx.send(err_msg)


@bot.command()
async def AddQuestion(ctx, class_name= None):
    """Prompts User to add Question to specific class"""
    #TODO: Should the user be prompted for the class if they don't enter it?
    if class_name == None:
        await ctx.send("Usage: !AddQuestion [className]")
    else:
        msg = await get_input(ctx, "what's the question?",30)
        dbu.add_question(ctx.message.author.id,msg)

    if msg != 0:
        await ctx.send(f'you said {msg}')


#TODO: needs further testing
@bot.command()
async def AnswerQuestion(ctx, question_id=None):
    """Answer a question given its id"""
    if question_id == None:
        await ctx.send("Usage: !AnswerQuestion [questionID]")
    else:
        #TODO: Should we print the question?
        msg = await get_input(ctx, "What's your answer to the question?",30)
        dbu.answer_question(ctx.message.author.id,question_id,msg)


#TODO: needs further testing
@bot.command()
async def GetQuestion(ctx):
    """Return a random question from your class"""
    # if its nothing then get question from any other the user's classes
    await ctx.send("Question ID: "+str(dbu.get_question(ctx.message.author.id)[0])+"\n"+str(dbu.get_question(ctx.message.author.id)[1]))


#TODO: implement get all answers for a question (HMMMM)
@bot.command()
async def GetAnswers(ctx, question_id=None):
    """Get answers for a specific question"""
    if question_id == None:
        await ctx.send("Command requires a question id --> ex. '!AnswerQuestion 1101'")
    else:
        msg = ""
        answerValues = db_utils.get_answer(question_id)
        answerIds = answerValues[0]
        answerTexts = answerValues[1]
        inc = 0
        for answerID in answerIds: 
            msg = "[A "+str(answerID[0])+"] "+str(answerTexts[inc][0])
            await ctx.send(msg)
            inc += 1
        return


# TODO: needs further testing
@bot.command()
async def GetClasses(ctx):
    """Returns a list of all classes"""
    class_name_tuples = db_utils.select_class_names()
    msg = ""
    for tuple in class_name_tuples:
        msg += tuple[0] + '\n'
    await ctx.send(msg)
    return


# generate a report of all data and send it a csv
# TODO: needs further testing
@bot.command()
async def GetReport(ctx):
    # NOTE: probably shouldn't include user data within CSV file, maybe only questions and answers
    """Generate a CSV report containing all information within the database"""
    dbu.generate_csv()
    file = discord.File("./quizbot_report.csv")
    await ctx.send(file=file, content="csv report")
    return


bot.run(TOKEN)
