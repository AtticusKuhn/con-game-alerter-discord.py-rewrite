from discord.ext import commands

import discord_utils.embeds as embeds
import methods

import sqlite3

class Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='alert-me',
        description='get reminded when the next game of con starts',
        aliases=['a'],
        usage="a ww3"
    )
    async def alert(self, ctx,format="all"):
        parsed_format=methods.parse_format(format)
        if not parsed_format:
            return await ctx.send(embed=embeds.simple_embed(False,"invalid format"))
        with open('data/alertpeople.txt', "r") as f:
            people_array=f.read().split("\n")
            if  f'{ctx.author.id} {format}' in people_array:
                people_array.remove(f'{ctx.author.id} {format}')
                await ctx.send(embed=embeds.simple_embed(False,"you will now be deleted from the alert list"))
            else:
                people_array.append(f'{ctx.author.id} {format}')
                await ctx.send(embed=embeds.simple_embed(True,"You will be alerted when the next game starts"))
        with open('data/alertpeople.txt', "w") as f:
            f.write("\n".join(people_array))
   # @commands.command(
   #     name='set-alert-channel',
   #     description='set a channel where new games will be announced',
   #     aliases=['sac'],
   #     usage="sac #con-games"
   # )
   # @commands.has_permissions(manage_channels=True)
   # async def set_alert_channel(self, channel: discord.textChannel) :

def setup(bot):
    bot.add_cog(Alerts(bot))