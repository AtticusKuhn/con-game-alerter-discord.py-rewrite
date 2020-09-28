from discord.ext import commands
from datetime import datetime as d
from discord_utils.embeds import simple_embed,dict_to_embed
#import discord 
import discord_utils.embeds as embeds

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
        print("help called with cog", cog)
        if cog=="":
            return_dict = {}
            for command in self.bot.commands:
                name = command.cog.__class__.__name__
                if not name in return_dict:
                    return_dict[name] = ""
                if ctx.message.content == "!con h":
                    return_dict[name] += f'{", ".join(command.aliases)},\n'
                else:
                    return_dict[name] += f'{str(command)},\n'
            for command in return_dict:
                return_dict[command]= return_dict[command][:-2]
            return_dict["helpful tips"] = '\n remember that to see commands relating to a specific module, you can do help {module name}. \n also to get info on a command do info {command name}'
            return await ctx.send(embed=dict_to_embed(return_dict))
        if not cog in self.bot.cogs:
            return await ctx.send(embed=simple_embed(False,f'Unrecognized module. The recognized modules are {", ".join(self.bot.cogs)}'))
        return_commands = []
        for command in self.bot.commands:
            if command.cog.__class__.__name__ == cog:
                return_commands.append(command)
        if ctx.message.content == "!con h":
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
            return await ctx.send(embed=simple_embed(True,f'name: {command.name}\n description:{command.description}\n aliases:{", ".join(command.aliases)}\n {"usage: "+command.usage if command.usage is not None else ""}'))
        return await ctx.send(embed=simple_embed(False,"can't find command"))
    @commands.command(
        name='invite',
        description='invite this bot to your server',
        aliases=['inv', 'invitelink'],
        usage="inv"
    )
    async def invite(self, ctx):
        await ctx.send(embed=simple_embed(True,"invite this bot with https://discord.com/oauth2/authorize?client_id=698691997279584338&permissions=117824&scope=bot"))


def setup(bot):
    bot.add_cog(Basic(bot))