from discord.ext import commands
from datetime import datetime
import time

import discord_utils.embeds as embeds
from scraper.request_game import get_global_games

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
        result = await get_global_games()
        print(result)
        games = result["result"]["games"]
        if format !="all":
            if format=="ww3" or format=="world war 3":
                games=list(filter(lambda game:game["properties"]["title"]=="WORLD WAR 3",games))
            else:
                games=list(filter(lambda game:game["properties"]["title"]==format,games))
        if sort=="newest":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["startofgame2"]) ) 
        elif sort=="empty":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["openSlots"]) ) 
        game=sorted_games[0]["properties"]
        reply = game["gameID"]
        ts = int(game["startofgame2"])
        await ctx.send(embed=embeds.simple_embed(True,f'Game {reply} has just started at time {datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]} You can join it by going to https://www.conflictnations.com/play.php?bust=1&gameID={reply}'))

def setup(bot):
    bot.add_cog(Global(bot))