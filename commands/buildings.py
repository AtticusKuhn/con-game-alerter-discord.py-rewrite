from discord.ext import commands
import json

import discord_utils.embeds as embeds
from methods import seconds_to_time, parse_costs

class Buildings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='building',
        description='get info on a building',
        aliases=['bl'],
        usage="bl 0 Arms Industry"
    )
    async def info_building(self, ctx,level:int=0,  *building_name:str):
        building_name = " ".join(building_name)
        print(building_name,level)
        with open('data/buildings.json') as json_file:
            data = json.load(json_file)
            found_buildings= list(filter(lambda unit:unit["upgrName"]["en"].lower()==building_name.lower(), data))
            if len(found_buildings)==0:
                return await ctx.send(embed=embeds.simple_embed(False,"cannot find unit"))
            found_buildings = found_buildings[0]
            del found_buildings["@c"]
            if "buildTime" in found_buildings:
                found_buildings["buildTime"]= str(seconds_to_time(int(found_buildings["buildTime"])))
                print("buildtime is now",found_buildings["buildTime"] )
            if "costs" in found_buildings:
                found_buildings["costs"]=parse_costs(found_buildings["costs"])
                print("costs is now",found_buildings["costs"] )
            if "dailyCosts" in found_buildings:
                found_buildings["dailyCosts"]=parse_costs(found_buildings["dailyCosts"])
                print("dailyCosts is now",found_buildings["costs"] )
            return await ctx.send(embed=embeds.dict_to_embed(found_buildings, f'https://www.conflictnations.com/clients/con-client/con-client_live/images/map/features/{found_buildings["featureIconPrefix"]}4.png?1598270165'))

def setup(bot):
    bot.add_cog(Buildings(bot))