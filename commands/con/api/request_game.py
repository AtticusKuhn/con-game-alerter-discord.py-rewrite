from discord.ext import commands
from datetime import datetime
import time
import json

import discord_utils.embeds as embeds
from api.con_api import request_game, get_players_in_game, game_news

class Request_game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @commands.command(
        name='active',
        description='see when a player last logged on',
        aliases=['infc', "info_country", "act", "online", "last_login"],
        usage="infc 3320203 Sweden"
    )
    async def info_country(self, ctx, game_id:int,country):
        result = await request_game(game_id)
        if "players" not in result:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that id")) 
        players = result["players"]
        del players["@c"]
        found=False
        for number, player in players.items():
            # print("player is", player)
            if player["name"] == country or ("nationName" in player and player["nationName"]==country):
                found=True
                break
        if not found:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that country"))
        player =  {
            "nation name":player["nationName"],
            "computer player":player["computerPlayer"],
            "lastLogin":player["lastLogin"],
            "defeated":player["defeated"],
            "is a golder?":player["premiumUser"],
            "activity":player["activityState"]
        }
        if "lastLogin" in player:
            if player["lastLogin"]!=0:
                if( player["lastLogin"] > time.time()):
                    excess_time = player["lastLogin"]-time.time()
                    excess_time = excess_time/3
                    start_date = time.time()-excess_time
                    player["lastLogin"] = start_date+excess_time
                player["lastLogin"] = datetime.fromtimestamp(player["lastLogin"]).strftime('%Y-%m-%d %H:%M:%S')
        return await ctx.send(embed=embeds.dict_to_embed(player,f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/big_{player["nation name"].lower().replace(" ","_")}.png?'))
    @commands.command(
        name='game_players',
        description='see which players have joined a game',
        aliases=['gpl'],
        usage="gpl 3320203"
    )
    async def game_players(self, ctx, game_id:int):
        result = await get_players_in_game(game_id)
        sep_char  = " " if ("-compress" in ctx.message.flags) else ",\n"
        if len(result["result"])==0:
            return await ctx.send(embed=embeds.simple_embed(False, "could not find game"))
        formatted= f'found {len(result["result"]["logins"])} players \n'+ sep_char.join(list(map( lambda x: x["login"],result["result"]["logins"])))
        return await ctx.send(embed=embeds.simple_embed(True, formatted))
    @commands.command(
        name='inactive-players',
        description='see which players in a game are',
        aliases=["inp"],
        usage="inp 3320203"
    )
    async def inactive_players(self, ctx, game_id:int):
        game = await request_game(game_id)
        if "players" not in game:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that id")) 
        players = game["players"]
        del players["@c"]
        inactive_players = list(filter(lambda player: not player[1]["active"],players.items() ))
        formatted_players  = "\n".join(list(map(lambda player: f'{player[1]["nationName"]} - {player[1]["activityState"]}', inactive_players)))
        return await ctx.send(embed=embeds.simple_embed(True, "The following players are vunerable to attack\n"+formatted_players)) 
    @commands.command(
        name='gamenews',
        description='get news of game',
        aliases=["gn"],
        usage="gn 3320203"
    )
    async def get_game_news(self, ctx, game_id:int):
        game= await game_news(game_id)
        print("game", game)
        return "success"
def setup(bot):
    bot.add_cog(Request_game(bot))