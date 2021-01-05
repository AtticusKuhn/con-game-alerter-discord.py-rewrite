from discord.ext import commands

import discord_utils.embeds as embeds
from api.con_api import get_player_ranking

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='player',
        description='get the stats on a player by username',
        aliases=['pl'],
        usage="pl TheB2"
    )
    async def player(self, ctx, *player_name):
        player_name=" ".join(player_name)
        if player_name == "" or player_name==" ":
            return await ctx.send(embed=embeds.simple_embed(False,"that is an invalid player name"))
        # print("player called")
        result = await get_player_ranking(player_name)
        print(result, "result")
        # print("result", result["result"])
        if not result:
            return await ctx.send(embed=embeds.simple_embed(False,"can't find that player"))
        ranking= result["result"]["rankProgress"]
        stats = result["result"]["gameStats"]["gameStatsScore"]
        ranking.update(stats)
        if "alliance" in result["result"]:
            ranking.update({"Alliance":result["result"]["alliance"]["properties"]["name"]})
        return await ctx.send(embed=embeds.dict_to_embed(ranking))

def setup(bot):
    bot.add_cog(Player(bot))