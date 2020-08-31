from discord.ext import commands
from datetime import datetime
import time

import discord_utils.embeds as embeds
from scraper.request_game import get_player_ranking

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='player',
        description='get the stats on a player by username',
        aliases=['pl'],
        usage="pl TheB2"
    )
    async def player(self, ctx, player_name):
        print("player called")
        result = await get_player_ranking(player_name)
        ranking= result["result"]["rankProgress"]
        stats = result["result"]["gameStats"]["gameStatsScore"]
        ranking.update(stats)
        return await ctx.send(embed=embeds.dict_to_embed(ranking))
        
def setup(bot):
    bot.add_cog(Player(bot))