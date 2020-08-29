from discord.ext import commands

import discord_utils.embeds as embeds
from scraper.request_game import request_game

class Request_game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='info_conutry',
        description='see when a player last logged on',
        aliases=['infc'],
        usage="infc 3320203 Sweden"
    )
    async def info_conutry(self, ctx, game_id:int,country):
        result = await request_game(game_id)
        if "players" not in result:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that id")) 
        players = result["players"]
        found=False
        for number, player in players.items():
            if player["name"] == country or player["nationName"]==country:
                found=True
                found_player=player
                break
        if not found:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that country"))
        return await ctx.send(embed=embeds.dict_to_embed(found_player))

def setup(bot):
    bot.add_cog(Request_game(bot))