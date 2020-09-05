from discord.ext import commands
from datetime import datetime
import time

import discord_utils.embeds as embeds
from scraper.request_game import get_alliance

class Alliance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='alliance',
        description='get the stats on a alliance by username',
        aliases=['al'],
        usage="al Edge of Extinction"
    )
    async def alliance(self, ctx, *alliance_name):
        alliance_name=" ".join(alliance_name)
        print("alliance called")
        result = await get_alliance(alliance_name)
        stats = result["stats"]
        return await ctx.send(embed=embeds.dict_to_embed(stats))
        
def setup(bot):
    bot.add_cog(Alliance(bot))