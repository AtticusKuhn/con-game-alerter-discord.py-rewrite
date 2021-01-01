from discord.ext import commands
import random
import discord_utils.embeds as embeds
from methods import random_line
import json
import discord
import requests
import aiohttp# aiohttp should be installed if discord.py is
#from functools import partial# partial lets us prepare a new function with args for run_in_executor
from PIL import Image, ImageDraw,ImageFont,ImageChops
#import imgkit
from io import BytesIO# BytesIO allows us to convert bytes into a file-like byte stream.
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    #Bounding box given as a 4-tuple defining the left, upper, right, and lower pixel coordinates.
    #If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    x1,y1,x2,y2=bbox
    print("bbox is",bbox)
    if bbox:
        return im.crop((x1-10,y1-10,x2+20,y2+20))

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
    
    @commands.command(
        name='meme',
        description='get a random CoN meme',
        aliases=['me'],
        usage="me"
    )
    async def meme(self, ctx):
        print(random_line(open("data/memes.txt")))
        return await ctx.send(embed=embeds.simple_embed(True, "want to submit your own conflict of nations meme? DM eulerthedestroyer#2074 and he will put it in the CoN meme collection.", random_line(open("data/memes.txt")) ))
    @commands.command(
        name='quiz',
        description='get conflict of nations quiz',
        aliases=['qz'],
        usage="qz"
    )
    async def quiz(self, ctx):     
        quiz_type  =random.choice([
            "identify unit image",
            "identify unit description",
            "identify country flag"
        ]) 
        answer_type = random.choice(["open response", "multiple choice"])
        if quiz_type == "identify unit image":
            with open('data/units.json') as json_file:
                units = json.load(json_file)
                chosen_unit = random.choice(units)
                correct_answer = chosen_unit["unitName"]
                question = f'https://www.conflictnations.com/clients/con-client/con-client_live/images/warfare/2/{chosen_unit["identifier"]}_1_0.png?1593611138'
                incorrect_answers = list(map(lambda x: x["unitName"], random.sample(units, 3)))
        elif quiz_type == "identify unit description":
            with open('data/units.json') as json_file:
                units = json.load(json_file)
                chosen_unit = random.choice(units)
                correct_answer = chosen_unit["unitName"] 
                    
                question =  f'Identify the following unit: {chosen_unit["unitDesc"]}'
                incorrect_answers = list(map(lambda x: x["unitName"], random.sample(units, 3)))
        elif quiz_type == "identify country flag":
            with open('data/countriesfinal.txt') as json_file:
                countries = json.load(json_file)   
                chosen_country = random.choice(list(countries.keys()))
                correct_answer = chosen_country
                question = f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/big_{chosen_country.lower().replace(" ","")}.png?'
                incorrect_answers =random.sample(list(countries.keys()), 3)
        
        question_body = f'\n \n This question is of type {quiz_type}. You have 10 seconds to answer. \n '
        if answer_type == "multiple choice":
            incorrect_answers.append(correct_answer)
            question_body+= f'\n \n Your answer choices are {", ".join(incorrect_answers)}'        
        if question.startswith("http"):
            await ctx.send(embed=embeds.simple_embed(True, question_body, question))
        else:
            question_body = question+"\n" + question_body
            await ctx.send(embed=embeds.simple_embed(True, question_body))
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        response = await self.bot.wait_for('message', check=check)
        print("response is", response.content," and correct_answer is", correct_answer,response == correct_answer )
        if response.content == correct_answer:
            return await ctx.send(embed=embeds.simple_embed(True, "yay you got it correct"))
        else:
            return await ctx.send(embed=embeds.simple_embed(False, f'oof the correct answer was actually, {correct_answer}'))

    @commands.command(
        name='news',
        description='create your own fake news article',
        aliases=['article',"art"],
        usage="news north korea nukes everyone"
    )
    async def news(self, ctx, *, title):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send(embed=embeds.simple_embed(True, "ok now give me the article body"))
        response1 = await self.bot.wait_for('message', check=check)
        body=response1.content
        await ctx.send(embed=embeds.simple_embed(True, "ok now give me the country name"))
        response2 = await self.bot.wait_for('message', check=check)
        #async with ctx.typing():
        country = response2.content
        flag_response = requests.get(f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/small_{country.lower().replace(" ","")}.png?')
        flag = Image.open(BytesIO(flag_response.content))
        flag_size = 70, 80
        flag = flag.resize((34,30))
        img = Image.new("RGB", (800, 800), (255, 255, 255))
        #img = Image.open("data/article.png") #Replace infoimgimg.png with your background image.
        draw = ImageDraw.Draw(img)
        title_font = ImageFont.truetype("data/fonts/Exo2Semibold.otf", 33) #Make sure you insert a valid font from your folder.
        body_font = ImageFont.truetype("data/fonts/tinos.regular.ttf", 18)
        sub_font = ImageFont.truetype("data/fonts/tinos.italic.ttf", 16)
        def draw_underlined_text(draw, pos, text, font, **options):    
            twidth, theight = draw.textsize(text, font=font)
            lx, ly = pos[0], pos[1] + theight+2
            print("lx is ", lx,"and ly is", ly)
            print("twidth is",twidth)
            draw.text(pos, text,(0, 0, 0), font=font, **options)
            draw.line((lx, ly, lx + twidth, ly), fill ="black", width = 1)
            draw.text((lx + twidth, pos[1]), " - Offical government press release, 22:52",(0,0,0),font=font)
        # x1, y2 = draw.textsize(title, font=title_font)
        # x2, y2 = draw.textsize(body, font=body_font)
        draw.text((70, 35), title, (0, 0, 0), font=title_font) #draws Information
        draw.text((20, 85), body, (0, 0, 0), font=body_font)
        draw_underlined_text(draw, (12, 10), country, sub_font)
        img.paste(flag, (24, 40))
        img=trim(img)
        final_buffer = BytesIO()
        img.save(final_buffer, "png")# save into the stream, using png format.
        final_buffer.seek(0)# seek back to the start of the stream
        file = discord.File(filename="article_2.png", fp = final_buffer)
        await ctx.send(file=file)# send it
    @commands.command(
        name='message',
        description='create your own fake message',
        aliases=['msg',],
        usage="msg hi"
    )
    async def message(self, ctx, *, message):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        await ctx.send(embed=embeds.simple_embed(True, "ok now give me the country"))
        response1 = await self.bot.wait_for('message', check=check)
        country=response1.content
        img = Image.open("data/images/message2.png")
        font = ImageFont.truetype("data/fonts/Exo2Semibold.otf", 20) #Make sure you insert a valid font from your folder.
        draw = ImageDraw.Draw(img)
        draw.text((690, 108), message, (255, 255, 255), font=font) #draws Information
        draw.text((85, 40), country, (255, 255, 255), font=font) #draws Information

        flag_response1 = requests.get(f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/small_{country.lower().replace(" ","")}.png?')
        flag_response2 = requests.get(f'https://www.conflictnations.com/clients/con-client/con-client_live/images/flags/countryFlagsByName/big_{country.lower().replace(" ","")}.png?')
        bigflag = Image.open(BytesIO(flag_response2.content)).resize((100,60))
        smallflag = Image.open(BytesIO(flag_response1.content)).resize((40,30))
        img.paste(bigflag, (1325, 90))
        img.paste(smallflag, (25, 40))

        final_buffer = BytesIO()
        img.save(final_buffer, "png")# save into the stream, using png format.
        final_buffer.seek(0)# seek back to the start of the stream
        file = discord.File(filename="article_2.png", fp = final_buffer)
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(Fun(bot))