from discord.ext import commands
import json

import discord_utils.embeds as embeds
#from methods import seconds_to_time, parse_costs

class Countrys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='country',
        description='get info on a country',
        aliases=['co'],
        usage="co Afghanistan"
    )
    async def country(self, ctx, *country_name:str,):
        country_name = " ".join(country_name)
        with open('data/countriesfinal.txt') as json_file:
            data = json.load(json_file)
            if country_name not in data:
                return await ctx.send(embed=embeds.simple_embed(False,"cannot find country"))
            if "exists in" in data[country_name]:
                data[country_name]["exists in"] = ", ".join(data[country_name]["exists in"])
            return await ctx.send(embed=embeds.dict_to_embed(data[country_name], f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/big_{country_name.lower().replace(" ","")}.png?'))
    @commands.command(
        name='map',
        description='get a con map based on factors like cities',
        aliases=['mp'],
        usage="map ww3 citites"
    )
    async def map(self, ctx, mode ="ww3",score="cities"):
        with open('data/map.txt') as json_file:
            data = json.load(json_file)
            if mode == "index":
                ret_string = ""
                for mode in data:
                    ret_string+=f'\n\n{mode}'
                    for score in data[mode]:
                        ret_string+=f'\n\t\t-{score}'
                return await ctx.send(embed=embeds.simple_embed(True, ret_string))
            if mode not in data:
                return await ctx.send(embed=embeds.simple_embed(False, f'invalid mode. Valid modes are {", ".join(list(data.keys()))}'))
            if not score in data[mode]:
                return await ctx.send(embed=embeds.simple_embed(False, f'invalid score. Valid scores are {", ".join(list(data[mode].keys()))}'))
            return await ctx.send(embed=embeds.simple_embed(True, "I'm currently working on more modes such as blood and oil and rising tides. Expect them to be here soon.", data[mode][score]))


def setup(bot):
    bot.add_cog(Countrys(bot))