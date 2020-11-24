from discord.ext import commands
import json

import discord_utils.embeds as embeds

class Formats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='format',
        description='get info on a format',
        aliases=['f'],
        usage="f world war 3"
    )
    async def format(self, ctx, *, format_name):
        print(format_name)
        with open('data/formats.json') as json_file:
            data = json.load(json_file)
            found_formats = list(filter(lambda format:format["ingameName"].lower()==format_name.lower(), data))
            if len(found_formats)==0:
                return await ctx.send(embed=embeds.simple_embed(False,"cannot find format"))
            found_format = found_formats[0]
            del found_format["@c"]

            return await ctx.send(embed=embeds.dict_to_embed(found_format, f'https://www.conflictnations.com/fileadmin/templates/conflictnations/shared-client/images/maps/scenario_{found_format["itemID"]}_thumb.png'))

def setup(bot):
    bot.add_cog(Formats(bot))