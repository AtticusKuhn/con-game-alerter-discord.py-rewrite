from discord.ext import commands
import json

import discord_utils.embeds as embeds
from methods import random_line

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='meme',
        description='get a random CoN meme',
        aliases=['me'],
        usage="me"
    )
    async def meme(self, ctx):
        return await ctx.send(embed=embeds.simple_embed(True, "want to submit your own conflict of nations meme? DM eulerthedestroyer#2074 and he will put it in the CoN meme collection.", random_line(open("data/memes.txt")) ))
       

def setup(bot):
    bot.add_cog(Meme(bot))