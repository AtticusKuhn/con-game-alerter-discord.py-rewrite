from discord.ext import commands
import keep_alive
import os
import replit
##events
from events.error import command_error
from events.ready import ready
from events.command import command
from events.message import message
from data.config import CONFIG
import sys 
sys.setrecursionlimit(10**6) 
import discord
intents = discord.Intents.default()
intents.members = True

from unit_tests.test import run_tests
import asyncio

def get_prefix(client, message):
    prefixes = [CONFIG.prefix, "!com "]    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
    return commands.when_mentioned_or(*prefixes)(client, message)    # Allow users to @mention the bot instead of using a prefix when using a command.
 
bot = commands.Bot(        # Create a new bot                                     
    command_prefix=get_prefix,                              # Set the prefix
    description='A bot used for conflict of nations',                  # Set a description for the bot
    owner_id=464954455029317633,                            # Your unique User ID
    case_insensitive=True,
    intents=intents                                  # Make the commands case insensitive
)

def _print(self, message="oof"):
    if self.test:
        return
    print(message)
    if hasattr(self, 'log'):
        self.log+= f'{message}\n'
    else:
        self.log= f'{message}\n'
    self.log  =self.log[:1000]
bot.test=False
    
commands.Bot.print = _print

@bot.event
async def on_ready():
    await ready(bot)
@bot.event
async def on_command(ctx):
    await command(bot,ctx)
@bot.event
async def on_command_completion(ctx):
    print(ctx)
@bot.event
async def on_message(ctx):
    await message(bot,ctx)
@bot.event
async def on_command_error(ctx,error):
    await command_error(bot, ctx, error)


keep_alive.keep_alive()# Start the server
replit.clear()
bot.tests = asyncio.run(run_tests())
bot.print(bot.tests)
bot.run(os.environ.get('DISCORD_BOT_SECRET'), bot=True, reconnect=True)# Finally, login the bo

 