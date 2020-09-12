from discord.ext import commands
import json

import discord_utils.embeds as embeds
from methods import seconds_to_time, parse_costs
import requests
import os
API_KEY = os.environ.get('YOUTUBE_API_KEY')
class Video(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name='video',
        description='get a video based on a keyword',
        aliases=['vid', "movie"],
        usage="video weekend update"
    )       
    async def video(self, ctx, *, keyword):
        TheB2 = "UCglLeRRcX8Jnb-dh2pijZyQ"
        result = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={TheB2}&maxResults=1&q={keyword}&key={API_KEY}').json()
        return await ctx.send(f'https://youtu.be/{result["items"][0]["id"]["videoId"]}')
def setup(bot):
    bot.add_cog(Video(bot))