from discord.ext import commands
import json

import discord_utils.embeds as embeds
from methods import seconds_to_time, parse_costs

class Units(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='unit',
        description='get info on a unit',
        aliases=['u'],
        usage="u 0 Motorized Infantry"
    )
    async def info_country(self, ctx,level:int=0,  *unit_name:str):
        unit_name = " ".join(unit_name)
        print(unit_name,level)
        with open('data/units.json') as json_file:
            data = json.load(json_file)
            found_units = list(filter(lambda unit:unit["unitName"].lower()==unit_name.lower(), data))
            if len(found_units)==0:
                return await ctx.send(embed=embeds.simple_embed(False,"cannot find unit"))
            found_unit = found_units[0]
            del found_unit["@c"]
            if "buildTime" in found_unit:
                found_unit["buildTime"]= str(seconds_to_time(int(found_unit["buildTime"])))
                print("buildtime is now",found_unit["buildTime"] )
            if "costs" in found_unit:
                found_unit["costs"]=parse_costs(found_unit["costs"])
                print("costs is now",found_unit["costs"] )
            if "dailyCosts" in found_unit:
                found_unit["dailyCosts"]=parse_costs(found_unit["dailyCosts"])
                print("dailyCosts is now",found_unit["costs"] )
            return await ctx.send(embed=embeds.dict_to_embed(found_unit, f'https://www.conflictnations.com/clients/con-client/con-client_live/images/warfare/2/{found_unit["identifier"]}_1_0.png?1593611138'))

def setup(bot):
    bot.add_cog(Units(bot))