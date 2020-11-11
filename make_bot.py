from discord.ext import commands
##events
from events.error import command_error
from events.ready import ready
from events.command import command
from data.config import CONFIG
import sys 
from os import listdir
from os.path import isfile, join
cogs = list(map(lambda x: x[:-3],[f for f in listdir("commands") if isfile(join("commands", f))]))
import discord
from data.config import CONFIG
from time import time
from os import listdir
from os.path import isfile, join
cogs = list(map(lambda x: x[:-3],[f for f in listdir("commands") if isfile(join("commands", f))]))
import discord
from data.config import CONFIG
from time import time
from os.path import isfile, join
cogs = list(map(lambda x: x[:-3],[f for f in listdir("commands") if isfile(join("commands", f))]))
import discord
from data.config import CONFIG
from time import time
import glob

sys.setrecursionlimit(10**6) 
import discord
intents = discord.Intents.default()
intents.members = True
def get_prefix(client, message):
    prefixes = [CONFIG.prefix, "!com "]    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
    return commands.when_mentioned_or(*prefixes)(client, message)    # Allow users to @mention the bot instead of using a prefix when using a command.

def make_bot():
    bot = commands.Bot(        # Create a new bot                                     
        command_prefix=get_prefix,                              # Set the prefix
        description='A bot used for conflict of nations',                  # Set a description for the bot
        owner_id=464954455029317633,                            # Your unique User ID
        case_insensitive=True,
        intents=intents                                  # Make the commands case insensitive
    )
    bot.remove_command('help')    # Make sure to do this before loading the cogs
    cogs = glob.glob('./commands/**/*.py', recursive=True)
    parsed_cogs = list(map(lambda cog: cog.replace("/",".")[2:-3], cogs))
    #print("ready called")
    #bot.print(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.remove_command('help')    # Make sure to do this before loading the cogs
    for cog in parsed_cogs:
        # print("about to import", cog)
        bot.load_extension(cog)
    
    
    #on_ready = bot.event(on read)
    @bot.event
    async def on_ready():
        print("ready called")
        # return "e"
    @bot.event
    async def on_message(m):
        print("on_message")
        return "e"
    @bot.event
    async def on_error(e):
        print("error")
        return
    @bot.event
    async def on_command(ctx):
        print("on_command")
        return
        # await command(bot,ctx)
    # @bot.event
    # async def on_command_error(ctx,error):
    #     await command_error(bot, ctx, error)
    return bot
