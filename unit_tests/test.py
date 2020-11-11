# import bruh as dpytest
# import dpytest
# import dpytest
# a = __import__("dpytest")
import bruh.ext.test as dpytest
#from test_bot import make_bot
import pytest
#from bruh.runner import get_config
from discord.ext import commands
#from commands.basic import Basic
#from bruh.runner import message
from make_bot import make_bot
#from commands import basic
import asyncio

from unit_tests.generate_tests import tests

# async def main():
#     bot = commands.Bot(command_prefix='?')
#     bot.load_extension("commands.universal.basic")
#     # Load any extensions/cogs you want to in here

#     dpytest.configure(bot)

#     await dpytest.message("?bruh")
#     dpytest.verify_message("[Expected help output]")
# asyncio.run( main())

# @pytest.mark.asyncio
async def run_tests():
    bot = commands.Bot(command_prefix='?')
    bot.remove_command("help")
    bot.load_extension("commands.universal.basic")
    # Load any extensions/cogs you want to in here

    dpytest.configure(bot)

    await dpytest.message("?ping")
    dpytest.verify_message("[Expected help output]")
    return
    # assert help_embed is not None
    # bot = make_bot()
    # #bot.test = True
    # dpytest.configure(bot,10 ,10, 10)
    # await dpytest.message("!con help")

    # return_arrray=[]
    # for test in tests:
    #     try:
    #         result = await test.run()
    #     except Exception as e:
    #         result = {"success":False, "comment":e}
    #     success = result["success"]
    #     comment = result["comment"]
    #     return_arrray.append({"name":test.name, "success":success, "comment":comment}) 
    #     #print(comment)
    # return return_arrray














    # await dpytest.message("!con help")
    # help_embed = dpytest.get_embed()
    # print("help_embed",help_embed)
    # assert help_embed is not None
