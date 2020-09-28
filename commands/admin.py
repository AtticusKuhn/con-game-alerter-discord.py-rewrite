from discord.ext import commands
#from datetime import datetime
#import time

import discord_utils.embeds as embeds
from scraper.request_game import get_alliance
from discord_utils.converters import PersonConverter
async def is_owner(ctx):
    return ctx.author.id == 464954455029317633
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name='say-as',
        description='say something on the behalf of someone else',
        aliases=['say'],
        usage="say eulerthedestroyer !con help"
    )
    @commands.check(is_owner)
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
        usage="servers"
    )
    async def server(self, ctx, *, server):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        found_server= False
        activeservers = self.bot.guilds
        for guild in activeservers: 
            if guild.name == server:
                found_server=guild
                break
        if not found_server:
            return await ctx.send(embed=embeds.simple_embed(False, "can't find server"))
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

        return await ctx.send(embed=embeds.dict_to_embed(ret_dict,found_server.icon_url ))
    @commands.command(
        name='previous',
        description='repeat the previous command you said',
        aliases=['pre', "prev", "^"],
        usage="pre"
    )
    async def previous(self, ctx):
        if ctx.author.id !=464954455029317633:
            return await ctx.send(embed=embeds.simple_embed(False, "only eulerthedestroyer#2074 can use admin commands"))
        async for message in ctx.channel.history(limit=200):
            if message.id == ctx.message.id:
                continue
            if message.author == ctx.author:
                if message.content.startswith("!con "):
                    if len(message.content.split(" ")) == 2:
                        return await ctx.invoke(self.bot.get_command(message.content.split(" ")[1]))
                    print('message.content.split(" ")[1] is',message.content.split(" ")[1])
                    print('" ".join(message.content.split(" ")[2:]) is'," ".join(message.content.split(" ")[2:]))
                    await ctx.invoke(self.bot.get_command(message.content.split(" ")[1])," ".join(message.content.split(" ")[2:]))
def setup(bot):
    bot.add_cog(Admin(bot))