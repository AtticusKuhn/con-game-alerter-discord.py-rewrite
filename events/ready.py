import replit
from intervals import check_for_alerts, set_interval
#from threading import Thread
from os import listdir
from os.path import isfile, join
cogs = list(map(lambda x: x[:-3],[f for f in listdir("commands") if isfile(join("commands", f))]))
import discord
from data.config import CONFIG


async def ready(bot):
    replit.clear()
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    bot.remove_command('help')    # Make sure to do this before loading the cogs
    for cog in cogs:
        print("cog is",cog)
        bot.load_extension(f'commands.{cog}')
    await bot.change_presence(activity=discord.Game(name=f'{CONFIG.prefix}help for help'))
    await set_interval(await check_for_alerts(bot), 10, bot)
    return