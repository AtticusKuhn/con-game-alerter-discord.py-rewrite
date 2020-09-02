from discord.ext import commands
from datetime import datetime

import discord_utils.embeds as embeds
from scraper.request_game import get_global_games
import methods

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='game',
        description='get a game based on properties like starttime',
        aliases=['g'],
        usage="game newest flashpoint"
    )
    async def game(self, ctx, sort="newest", format="all"):
        if format !="all":
            if not methods.parse_format(format):
                return await ctx.send(embed=embeds.simple_embed(False,"not a valid format"))
            format = methods.parse_format(format)
        result = await get_global_games()
        print(result)
        games = result["result"]["games"]
        games =list(filter(lambda game:game["title"]==format, games))
        if sort=="newest":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["startofgame2"]) ) 
        elif sort=="empty":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["openSlots"]) ) 
        if len(sorted_games)==0:
            return await ctx.send(embed=embeds.simple_embed(False,"can't find any games"))
        game=sorted_games[0]["properties"]
        reply = game["gameID"]
        ts = int(game["startofgame2"])
        await ctx.send(embed=embeds.simple_embed(True,f'Game {reply} has just started at time {datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]} You can join it by going to https://www.conflictnations.com/play.php?bust=1&gameID={reply}'))

def setup(bot):
    bot.add_cog(Global(bot))