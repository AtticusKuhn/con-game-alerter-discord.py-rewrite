from discord.ext import commands
from datetime import datetime

import discord_utils.embeds as embeds
import discord_utils.converters as converters
from scraper.request_game import get_global_games
import methods

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='list_games',
        description='get a list of games based on properties like starttime',
        aliases=['lg', "games", "multiple games", "list games"],
        usage="list_games newest flashpoint"
    )
    async def list_games(self, ctx, sort="newest", *, format:converters.FormatConverter="all"):
        result = await get_global_games()
        games = result["result"]["games"]
        if format != "all":
            print("format is ", format)
            games =list(filter(lambda game:game["properties"]["title"]==format, games))
        if sort=="newest":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["startofgame2"]) ) 
        elif sort=="empty":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["openSlots"]) )
        else:
            return await ctx.send(embed=embeds.simple_embed(False, "invalid sorting. Try perhaps newest or empty"))
        if len(sorted_games)==0:
            return await ctx.send(embed=embeds.simple_embed(False,"can't find any games"))
        games=list(map(lambda game: game["properties"], games))
        return_dict = {}
        for index, game in enumerate(games):
            reply = game["gameID"]
            ts = int(game["startofgame2"])
            return_dict[index+1] = f'Game {reply} has just started at time {datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]}.'
        await ctx.send(embed=embeds.dict_to_embed(return_dict))

    @commands.command(
        name='game',
        description='get a game based on properties like starttime',
        aliases=['g'],
        usage="game newest flashpoint"
    )
    async def game(self, ctx, sort="newest", *, format:converters.FormatConverter="all"):
        result = await get_global_games()
        games = result["result"]["games"]
        if format != "all":
            print("format is ", format)
            games =list(filter(lambda game:game["properties"]["title"]==format, games))
        if sort=="newest":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["startofgame2"]) ) 
        elif sort=="empty":
            sorted_games = sorted(games, key=lambda game: -int(game["properties"]["openSlots"]) )
        else:
            return await ctx.send(embed=embeds.simple_embed(False, "invalid sorting. Try perhaps newest or empty"))
        if len(sorted_games)==0:
            return await ctx.send(embed=embeds.simple_embed(False,"can't find any games"))
        game=sorted_games[0]["properties"]
        reply = game["gameID"]
        ts = int(game["startofgame2"])
        await ctx.send(embed=embeds.simple_embed(True,f'Game {reply} has just started at time {datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]} You can join it by going to https://www.conflictnations.com/play.php?bust=1&gameID={reply}'))
        
def setup(bot):
    bot.add_cog(Global(bot))