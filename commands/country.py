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

def setup(bot):
    bot.add_cog(Countrys(bot))