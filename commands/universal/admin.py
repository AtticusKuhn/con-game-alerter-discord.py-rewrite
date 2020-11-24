from discord.ext import commands
#from datetime import datetime
#import time

import discord_utils.embeds as embeds
from discord_utils.converters import PersonConverter
from time import time
import math
from methods import seconds_to_time
from datetime import datetime as d
import discord
import os
import traceback

async def is_owner(ctx):
    return ctx.author.id == 464954455029317633
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name='say-as',
        description='say something on the behalf of someone else',
        aliases=['say'],
        usage="say eulerthedestroyer help"
    )
    async def say(self, ctx, person:PersonConverter, *, message):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        ctx.author = person
        if len(message.split(" ")) == 1:
            return await ctx.invoke(self.bot.get_command(message.split(" ")[0]))
        await ctx.invoke(self.bot.get_command(message.split(" ")[0])," ".join(message.split(" ")[1:]))
    @commands.command(
        name='servers',
        description='see all servers this bot is in',
        aliases=['guilds'],
        usage="servers"
    )
    async def servers(self, ctx):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        ret_string=""
        activeservers = self.bot.guilds
        for guild in activeservers:
            ret_string += guild.name+"\n"
        return await ctx.send(embed=embeds.simple_embed(True,ret_string))
    @commands.command(
        name='server',
        description='get info on a server this bot is in',
        aliases=['guild'],
        usage="server"
    )
    async def server(self, ctx, *, server=None):
        if server == None:
            server = ctx.guild.name
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        found_server= False
        found_server = [guild for guild in self.bot.guilds if guild.name == server]
        if len(found_server)==0:
            return await ctx.send(embed=embeds.simple_embed(False, "can't find server"))
        found_server = found_server[0]
        ret_dict = {}
        ret_dict["members"] = list(map(lambda x: x.name, found_server.members))
        for channel in found_server.channels:
            try:
                link = await channel.create_invite(max_age = 300)
                break
            except:
                continue
        ret_dict["invite"] = link
        ret_dict["name"] =found_server.name
        ret_dict["channels"] = list(map(lambda x: x.name, found_server.channels))
        ret_dict["roles"] = list(map(lambda x: x.name, found_server.roles))

        return await ctx.send(embed=embeds.dict_to_embed(ret_dict,found_server.icon_url ))
    
    @commands.command(
        name='dashboard',
        description='display important stats',
        aliases=['db'],
        usage="db"
    )
    async def dashboard(self, ctx):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        start = d.timestamp(d.now())
        ret_dict={}
        ret_dict["uptime"]=f':green_circle: Online for {seconds_to_time(math.floor(time()-self.bot.startup_time))}'
        ret_dict["Commands responded"] = self.bot.commands_responded
        ret_dict["errors"] = self.bot.command_errors
        ret_dict["servers"] = len(self.bot.guilds)
        ret_dict["unit tests"] = self.bot.tests
        ret_dict["latency"] = "pinging...."
        msg = await ctx.send(embed=embeds.dict_to_embed(ret_dict ))
        ret_dict["latency"] =f'{math.floor((d.timestamp(d.now())-start) * 1000)} ms'
        await msg.edit(embed=embeds.dict_to_embed(ret_dict ))
    @commands.command(
        name='exec',
        description='execute arbitrary code',
        aliases=['execute',"evaluate","eval"],
        usage="exec ```py \n print('e')```"
    )
    async def _exec(self, ctx, *,code):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        if code.startswith("```python") and code.endswith("```"):
            code=code[9:-3]
        elif code.startswith("```py") and code.endswith("```"):
            code=code[5:-3]
        elif code.startswith("```") and code.endswith("```"):
            code=code[3:-3]
        print("final code is ", code)
 
        exec_dict = {
            "bot":self.bot,
            "self":self,
            "ctx":ctx,
            "code":code,
            "discord":discord,
            "time":time,
            # "print":fake_print,
            "os":os,
            "methods":__import__("methods")
        }
        async def aexec(code, context):
            exec_code=f'async def __ex(): ' +''.join(f'\n {l}' for l in code.split('\n')
            )+'''\n if "output" in locals():\n  return output'''
            def fake_print(message):
                print("fakeprint called")
                context["output"] = message
            context["print"] = fake_print
            try:    
                exec(
                    exec_code
                ,context)
                res = await context['__ex']()
            except Exception as error:
                etype = type(error)
                trace = error.__traceback__
                verbosity = 4
                lines = traceback.format_exception(etype, error, trace, verbosity)
                traceback_text = ''.join(lines)
                res = f'error:``` \n {traceback_text} ```'
            print("res",res)
            return res
        result = await aexec(code,exec_dict)

        return await ctx.send(embed=embeds.simple_embed(result == None or not str(result).startswith("error"), f'output: {result}'))
    @commands.command(
        name='log',
        description='see the bot log',
        aliases=["logs"],
        usage="log"
    )
    async def return_log(self, ctx):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        return await ctx.send(embed=embeds.simple_embed(True, self.bot.log))

    @commands.command(
        name='speak',
        description='get the bot to speak',
        usage="speak hello"
    )
    async def speak(self, ctx, *, message):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        m = await ctx.send(message)
        #await m.delete()
        try:
            await ctx.message.delete()
        except:
            pass
def setup(bot):
    bot.add_cog(Admin(bot))