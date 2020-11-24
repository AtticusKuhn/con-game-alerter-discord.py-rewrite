from discord.ext import commands
from api.youtube_api import search_video
import discord_utils.embeds as embeds

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
        result = await search_video(TheB2, keyword)
        if not result["success"]:
            return await ctx.send(embed=embeds.simple_embed(False, result["message"]))
        return await ctx.send(f'https://youtu.be/{result["message"]}')
def setup(bot):
    bot.add_cog(Video(bot))