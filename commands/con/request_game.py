from discord.ext import commands
from datetime import datetime
import time

import discord_utils.embeds as embeds
from scraper.request_game import request_game, get_players_in_game

class Request_game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @commands.command(
        name='active',
        description='see when a player last logged on',
        aliases=['infc', "info_country", "act", "online", "login"],
        usage="infc 3320203 Sweden"
    )
    async def info_country(self, ctx, game_id:int,country):
        return await ctx.send(embed=embeds.simple_embed(False,"this command does not work and it is currently broken")) 

        result = await request_game(game_id)
        if "players" not in result:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that id")) 
        players = result["players"]
        del players["@c"]
        found=False
        for number, player in players.items():
            print("number",number)
            print("player",player)
            if player["name"] == country or player["nationName"]==country:
                found=True
                found_player=player
                break
        if not found:
            return await ctx.send(embed=embeds.simple_embed(False,"cannot find that country"))
        del player["@c"]
        if "lastLogin" in player:
            if player["lastLogin"]!=0:
                if( player["lastLogin"] > time.time()):
                    excess_time = player["lastLogin"]-time.time()
                    excess_time = excess_time/3
                    start_date = time.time()-excess_time
                    player["lastLogin"] = start_date+excess_time
                player["lastLogin"] = datetime.fromtimestamp(player["lastLogin"]).strftime('%Y-%m-%d %H:%M:%S')
        return await ctx.send(embed=embeds.dict_to_embed(found_player,f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/big_{found_player["nationName"].lower().replace(" ","_")}.png?'))
    @commands.command(
        name='game_players',
        description='see which players have joined a game',
        aliases=['gpl'],
        usage="gpl 3320203"
    )
    async def game_players(self, ctx, game_id:int):
        result = await get_players_in_game(game_id)
        print(result)
        if len(result["result"])==0:
            return await ctx.send(embed=embeds.simple_embed(False, "could not find game"))
        formatted= f'found {len(result["result"]["logins"])} players \n'+ ",\n".join(list(map( lambda x: x["login"],result["result"]["logins"])))
        return await ctx.send(embed=embeds.simple_embed(True, formatted))
def setup(bot):
    bot.add_cog(Request_game(bot))