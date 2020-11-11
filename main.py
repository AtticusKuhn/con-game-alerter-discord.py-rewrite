from discord.ext import commands
# Import the keep alive file
import keep_alive
import os
import bruh.ext.test as dpytest
##events
from events.error import command_error
from events.ready import ready
from events.command import command
from data.config import CONFIG
import sys 
sys.setrecursionlimit(10**6) 
import discord
intents = discord.Intents.default()
intents.members = True

# import asyncio
# async def main():
#     bot = commands.Bot(command_prefix='?')
#     bot.remove_command("help")
#     bot.load_extension("commands.universal.basic")
#     # Load any extensions/cogs you want to in here

#     dpytest.configure(bot)

#     await dpytest.message("?ping")
#     dpytest.verify_message("[Expected help output]")
from unit_tests.tests import run_tests
import asyncio
asyncio.run(run_tests())

#from scraper.request_game import get_session
#print( get_session())
#sys.exit(0)
#import json
#with open("data/countriesfinal.txt", "r") as f:
#    countriesfinal = json.loads(f.read())
#with open("data/countriesoverkill.txt", "r") as f:
#    countries = json.loads(f.read())
#    for country in countries:
#        if not country["FIELD1"] in countriesfinal:
#           countriesfinal[country["FIELD1"]]={
#               "exists in":[]
#           } 
#        print(countriesfinal[country["FIELD1"]])
#        countriesfinal[country["FIELD1"]]["overkill cities"]=country["FIELD4"]
#        countriesfinal[country["FIELD1"]]["overkill vps"]=country["FIELD5"]
#        countriesfinal[country["FIELD1"]]["exists in"].append("overkill")
#with open("data/countriesfinal.txt","w") as f:
#    f.write(json.dumps(countriesfinal))

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
async def on_command_error(ctx,error):
    await command_error(bot, ctx, error)

keep_alive.keep_alive()# Start the server
token = os.environ.get('DISCORD_BOT_SECRET')
bot.run(token)# Finally, login the bot

 