from discord.ext import commands

import discord_utils.embeds as embeds
import methods

import json
from datetime import datetime
from time import time

class Alerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='alert-me',
        description='get reminded when the next game of con starts',
        aliases=['a'],
        usage="a ww3 time:12:10:03 uses:5"
    )
    async def alert(self, ctx,format="all", *options):
        parsed_format=methods.parse_format(format)
        if not parsed_format:
            return await ctx.send(embed=embeds.simple_embed(False,"invalid format"))
        with open('data/alertpeople2.txt', "r") as f:
            people=json.loads(f.read())
            if str(ctx.author.id) in people:
                del people[str(ctx.author.id)]
                await ctx.send(embed=embeds.simple_embed(False,"you will now be deleted from the alert list"))
            else:
                people[str(ctx.author.id)]={
                    "format":parsed_format
                }
                for option in options:
                    if option.startswith("time:"):
                        pt = datetime.strptime(option[5:],'%H:%M:%S')
                        people[str(ctx.author.id)]["time"]= pt.second + pt.minute*60 + pt.hour*3600 + time()
                    elif option.startswith("uses:"): 
                        try:
                            people[str(ctx.author.id)]["uses"]=int(option[5:])
                        except:
                            return await ctx.send(embed=embeds.simple_embed(False,"invalid uses amount"))
                    else:
                        return await ctx.send(embed=embeds.simple_embed(False, "invalid option"))
                await ctx.send(embed=embeds.simple_embed(True,f'You will be alerted when the next game starts'))
        with open('data/alertpeople2.txt', "w") as f:
            f.write(json.dumps(people))
   # @commands.command(
   #     name='set-alert-channel',
   #     description='set a channel where new games will be announced',
   #     aliases=['sac'],
   #     usage="sac #con-games"
   # )
   # @commands.has_permissions(manage_channels=True)
   # async def set_alert_channel(self, channel: discord.textChannel) :

def setup(bot):
    bot.add_cog(Alerts(bot))