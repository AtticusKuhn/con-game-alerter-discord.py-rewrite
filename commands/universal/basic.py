from discord.ext import commands
from datetime import datetime as d
from discord_utils.embeds import simple_embed,dict_to_embed
import discord_utils.embeds as embeds
from data.config import CONFIG
class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='ping',
        description='The ping command. Tests server lag',
        aliases=['p'],
        usage="p"
    )
    async def ping_command(self, ctx):
        start = d.timestamp(d.now())
        msg = await ctx.send(embed=embeds.simple_embed(False,"pinging......"))
        await msg.edit(embed=embeds.simple_embed(True,f'Pong!\nOne message round-trip took {(d.timestamp(d.now())-start) * 1000}ms.'))
        return
    @commands.command(
        name='help',
        description='gives a list of possible commands',
        aliases=['commands', "all-commands", "h"],
        usage="help"
    )
    async def help(self, ctx, cog=""):
        # print("help called with cog", cog)
        sep_char = ", " if "-compress" in ctx.message.flags["unnamed"] else ",\n"
        if cog=="":
            return_dict = {}
            for command in self.bot.commands:
                name = command.cog.__class__.__name__
                if not name in return_dict:
                    return_dict[name] = ""
                if ctx.message.content == f'{CONFIG.prefix} h':
                    return_dict[name] += f'{", ".join(command.aliases)}{sep_char}'
                else:
                    return_dict[name] += f'{str(command)}{sep_char}'
            for command in return_dict:
                return_dict[command]= return_dict[command][:-2]
            return_dict["helpful tips"] = '\n remember that to see commands relating to a specific module, you can do help {module name}. \n also to get info on a command do info {command name}'
            # print("help is done")
            return await ctx.send(embed=dict_to_embed(return_dict))
        if not cog in self.bot.cogs:
            return await ctx.send(embed=simple_embed(False,f'Unrecognized module. The recognized modules are {", ".join(self.bot.cogs)}'))
        return_commands = []
        for command in self.bot.commands:
            if command.cog.__class__.__name__ == cog:
                return_commands.append(command)
        if ctx.message.content == f'{CONFIG.prefix} h':
            return_commands=list(map(lambda c:f'{", ".join(command.aliases)} - {str(c.description)}',return_commands))
        else:
            return_commands=list(map(lambda c:f'{str(c)} - {str(c.description)}',return_commands))
        return await ctx.send(embed=simple_embed(True,"\n".join(return_commands)))

    @commands.command(
        name='info',
        description='gives info on a secpfic command',
        aliases=['information', 'i']
    )
    async def info(self, ctx, command_name):
        command = [c for c in self.bot.commands if c.name==command_name or command_name in c.aliases]
        if len(command)>0:
            command=command[0]
            filtered_dict = {k: v for k, v in command.__dict__.items() if not k.startswith('_') and k not in ["params","cog"]}
            return await ctx.send(embed=dict_to_embed(filtered_dict))
            # return await ctx.send(embed=simple_embed(True,f'name: {command.name}\n description:{command.description}\n aliases:{", ".join(command.aliases)}\n {"usage: "+command.usage if command.usage is not None else ""}'))
        return await ctx.send(embed=simple_embed(False,"can't find command"))
    @commands.command(
        name="module",
        description="get info on a specific module",
        aliases=["mo"],
        usage="mo universal"
    )
    async def module(self, ctx, module_name):
        found_commands = [c for c in self.bot.commands if  f'.{module_name}' in c.module]
        if len(found_commands) == 0 :
            return await ctx.send(embed=simple_embed(False,"can't find module"))
        return await ctx.send(embed = simple_embed(True, ",\n".join(list(map(lambda c:c.name, found_commands)))))
    @commands.command(
        name='invite',
        description='invite this bot to your server',
        aliases=['inv', 'invitelink'],
        usage="inv"
    )
    async def invite(self, ctx):
        await ctx.send(embed=simple_embed(True,"invite this bot with https://discord.com/oauth2/authorize?client_id=698691997279584338&permissions=117824&scope=bot"))
    @commands.command(
        name='previous',
        description='repeat the previous command you said',
        aliases=['pre', "prev", "^"],
        usage="pre"
    )
    async def previous(self, ctx):
        async for message in ctx.channel.history(limit=200):
            if message.id == ctx.message.id:
                continue
            if message.author == ctx.author:
                if message.content.startswith(CONFIG.prefix):
                    if len(message.content.split(" ")) == 2:
                        return await ctx.invoke(self.bot.get_command(message.content.split(" ")[1]))
                    print('message.content.split(" ")[1] is',message.content.split(" ")[1])
                    print('" ".join(message.content.split(" ")[2:]) is'," ".join(message.content.split(" ")[2:]))
                    await ctx.invoke(self.bot.get_command(message.content.split(" ")[1])," ".join(message.content.split(" ")[2:]))
                    return

def setup(bot):
    bot.add_cog(Basic(bot))