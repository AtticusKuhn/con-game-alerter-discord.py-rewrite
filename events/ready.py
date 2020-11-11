# import replit
from intervals import check_for_alerts, set_interval
#from threading import Thread
from os import listdir
from os.path import isfile, join
cogs = list(map(lambda x: x[:-3],[f for f in listdir("commands") if isfile(join("commands", f))]))
import discord
from data.config import CONFIG
from time import time
import glob
async def ready(bot):
    # replit.clear()
    cogs = glob.glob('./commands/**/*.py', recursive=True)
    parsed_cogs = list(map(lambda cog: cog.replace("/",".")[2:-3], cogs))
    print("ready called")
    bot.remove_command('help')    # Make sure to do this before loading the cogs
    for cog in parsed_cogs:
        ##print("about to import", cog)
        bot.load_extension(cog)
    bot.startup_time = time()
    bot.command_errors=0
    bot.commands_responded=0
    bot.commands_responded+=1
    if hasattr(bot, "user") and bot.user is not None:
        bot.print(f'Logged in as {bot.user.name} - {bot.user.id}')
        await bot.change_presence(activity=discord.Game(name=f'{CONFIG.prefix}help for help'))
        await set_interval(await check_for_alerts(bot), 10, bot)
    return