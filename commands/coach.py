from discord.ext import commands
import json
import discord
import discord_utils.embeds as embeds
from discord_utils.converters import PersonConverter
class Coach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='join',
        description="join a coach's team or waiting list ",
        aliases=['jn'],
        usage="join eulerthedestroyer"
    )
    async def join(self, ctx,  *, coach: PersonConverter):
        if coach.id == ctx.author.id:
            return await ctx.send(embed=embeds.simple_embed(False, f'you cannot join your own team'))  
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(coach.id) in coaches:
                coaches[str(coach.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
            if str(ctx.author.id) in coaches[str(coach.id)]["team"] or str(ctx.author.id) in coaches[str(coach.id)]["waiting"]:
                return await ctx.send(embed=embeds.simple_embed(False, f'you cannot apply twice.'))
            if len(coaches[str(coach.id)]["team"]) > coaches[str(coach.id)]["options"]["teamsize"] or coaches[str(coach.id)]["options"]["admit"]==False:
                coaches[str(coach.id)]["waiting"] = [*coaches[str(coach.id)]["waiting"],str(ctx.author.id)]
                await ctx.send(embed=embeds.simple_embed(True, f'you are {len(coaches[str(coach.id)]["waiting"])} on the waiting list'))
            else:
                coaches[str(coach.id)]["team"] =[*coaches[str(coach.id)]["team"], str(ctx.author.id)]
                await ctx.send(embed=embeds.simple_embed(True, f'you are on the team'))           
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
    @commands.command(
        name='coach',
        description="see your team and waiting list, or somone else",
        aliases=['ch',"team"],
        usage="my_coach"
    )
    async def my_coach(self, ctx,  *, coach: PersonConverter=None):
        if coach == None:
            coach = ctx.author 
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(coach.id) in coaches:
                coaches[str(coach.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
        coaches[str(coach.id)]["team"] = list(map(lambda person : f'<@{person}>', coaches[str(coach.id)]["team"])) 
        coaches[str(coach.id)]["waiting"] = list(map(lambda person : f'<@{person}>', coaches[str(coach.id)]["waiting"]))  
        return await ctx.send(embed=embeds.dict_to_embed(coaches[str(coach.id)]))    
    @commands.command(
        name='remove',
        description="delete someone from your team or waiting list",
        aliases=['rmv',"delete"],
        usage="remove eulerthedestroyer"
    )
    async def remove(self, ctx,  *, person: PersonConverter):
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(ctx.author.id) in coaches:
                coaches[str(ctx.author.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
        if str(person.id) in coaches[str(ctx.author.id)]["team"]:
            coaches[str(ctx.author.id)]["team"] = list(filter(lambda team :team != str(person.id), coaches[str(ctx.author.id)]["team"]))
            await ctx.send(embed=embeds.dict_to_embed(coaches[str(ctx.author.id)]))    
        elif str(person.id) in coaches[str(ctx.author.id)]["waiting"]:
            coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != str(person.id), coaches[str(ctx.author.id)]["waiting"]))
            await ctx.send(embed=embeds.dict_to_embed(coaches[str(ctx.author.id)])) 
        else:
            return await ctx.send(embed=embeds.simple_embed(False, f'cannot find that person in your team or waiting'))
        for person in coaches[str(ctx.author.id)]["waiting"]:
            if len(coaches[str(ctx.author.id)]["team"]) >= coaches[str(ctx.author.id)]["options"]["teamsize"]:
                break
            coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != person, coaches[str(ctx.author.id)]["waiting"]))
            coaches[str(ctx.author.id)]["team"] = [*coaches[str(ctx.author.id)]["team"], person]
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
    @commands.command(
        name='move',
        description="move someone to team, waiting, or off",
        aliases=['mv'],
        usage="move eulerthedestroyer team"
    )
    async def move(self, ctx,person: PersonConverter, *, area='off' ):
        if person.id == ctx.author.id:
            return await ctx.send(embed=embeds.simple_embed(False, f'you cannot join your own team'))  
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(ctx.author.id) in coaches:
                coaches[str(ctx.author.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
            coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != str(person.id), coaches[str(ctx.author.id)]["waiting"]))
            coaches[str(ctx.author.id)]["team"] = list(filter(lambda team :team != str(person.id), coaches[str(ctx.author.id)]["team"]))
            if area == "team":
                coaches[str(ctx.author.id)]["team"] =[*coaches[str(ctx.author.id)]["team"], str(person.id)]
            elif area == "waiting":
                coaches[str(ctx.author.id)]["waiting"] =[*coaches[str(ctx.author.id)]["waiting"], str(person.id)]
            elif area =="off":
                for person in coaches[str(ctx.author.id)]["waiting"]:
                    if len(coaches[str(ctx.author.id)]["team"]) >= coaches[str(ctx.author.id)]["options"]["teamsize"]:
                        break
                    coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != person, coaches[str(ctx.author.id)]["waiting"]))
                    coaches[str(ctx.author.id)]["team"] = [*coaches[str(ctx.author.id)]["team"], person]
            else:
                await ctx.send(embed=embeds.simple_embed(False, f'invalid area. You cannot move someone to an area that does not exist')) 
            await ctx.send(embed=embeds.dict_to_embed(coaches[str(ctx.author.id)]))           
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))

    @commands.command(
        name='coach_settings',
        description="switch the options of your coach team",
        aliases=['cs',"coach_options", "options"],
        usage="remove eulerthedestroyer"
    )
    async def coach_settings(self, ctx, setting_name, option):
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(ctx.author.id) in coaches:
                coaches[str(ctx.author.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
            if setting_name == "admit":
                option = (option.lower() == "true")
            elif setting_name == "teamsize":
                try:
                    option = int(option)
                except:
                    return await ctx.send(embed=embeds.simple_embed(False, f'teamsize must be an integer')) 
            else:
                return await ctx.send(embed=embeds.simple_embed(False, f'invalid setting name. The settings are teamsize and admit')) 
            coaches[str(ctx.author.id)]["options"][setting_name] = option
            await ctx.send(embed=embeds.dict_to_embed(coaches[str(ctx.author.id)]))           
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))



    @commands.command(
        name='clear_team',
        description="delete all people off your team",
        aliases=['delete-team',"clear-team", "delteam"],
        usage="delteam"
    )
    async def clear_team(self, ctx):
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(ctx.author.id) in coaches:
                coaches[str(ctx.author.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
            coaches[str(ctx.author.id)]["team"] = []
            for person in coaches[str(ctx.author.id)]["waiting"]:
                if len(coaches[str(ctx.author.id)]["team"]) >= coaches[str(ctx.author.id)]["options"]["teamsize"]:
                    break
                coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != person, coaches[str(ctx.author.id)]["waiting"]))
                coaches[str(ctx.author.id)]["team"] = [*coaches[str(ctx.author.id)]["team"], person]
            await ctx.send(embed=embeds.dict_to_embed(coaches[str(ctx.author.id)]))           
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))

def setup(bot):
    bot.add_cog(Coach(bot))