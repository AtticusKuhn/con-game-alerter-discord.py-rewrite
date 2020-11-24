from discord_utils.embeds import simple_embed 
import traceback
from discord.ext.commands import CommandNotFound
from Levenshtein import distance
import re
from discord import DiscordException
from data.config import CONFIG
async def command_error(bot, ctx, error):
    print(f'error: {error}')
    bot.command_errors+=1
    if isinstance(error, CommandNotFound):
        regex = re.search(r'".*"', str(error))
        if regex is not None:
            false_command = regex.group()
        else:
            false_command = ""
        dis=1000
        current_command=""
        for command in bot.commands:
            test_distance = distance(command.name, false_command)
            if  test_distance< dis:
                dis= test_distance
                current_command= command.name
            for alias in command.aliases:
                test_distance = distance(alias, false_command)
                if  test_distance< dis:
                    dis= test_distance
                    current_command= alias
        return await ctx.send(embed=simple_embed(False, f' I do not recognize that command. It is closest to the existing command "{current_command}". If you did not mean to use that then try {CONFIG.prefix}help'))
    if isinstance(error, DiscordException):
        print("the error was a discord error")
    print(error)
    await ctx.send(embed=simple_embed(False, str(error)))
    etype = type(error)
    trace = error.__traceback__
    verbosity = 4
    lines = traceback.format_exception(etype, error, trace, verbosity)
    traceback_text = ''.join(lines)
    print(traceback_text)
	