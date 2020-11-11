from discord.ext import commands
import json
import discord
import discord_utils.embeds as embeds
from discord_utils.converters import PersonConverter

def parse_ids(coach):
    with open('data/coach.txt', "r") as f:
        coaches=json.loads(f.read())
        coaches[str(coach.id)]["team"] = list(map(lambda person : f'<@{person}>', coaches[str(coach.id)]["team"])) 
        coaches[str(coach.id)]["waiting"] = list(map(lambda person : f'<@{person}>', coaches[str(coach.id)]["waiting"]))  
        return coaches[str(coach.id)]
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
                await ctx.send(embed=embeds.simple_embed(True, f'you are on the team of {coach.name}'))           
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
        await update_room_permissions(ctx.guild ,coach)
    
    @commands.command(
        name='leave',
        description="leave a coach's team or waiting list ",
        aliases=['lv'],
        usage="lv eulerthedestroyer"
    )
    async def leave(self, ctx,  *, coach: PersonConverter):
        if coach.id == ctx.author.id:
            return await ctx.send(embed=embeds.simple_embed(False, f'you cannot join your own team'))  
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if not str(coach.id) in coaches:
                coaches[str(coach.id)] = {"options":{"teamsize":5,"admit":True},"team":[],"waiting":[]}
            if str(ctx.author.id) not in coaches[str(coach.id)]["team"] or str(ctx.author.id) in coaches[str(coach.id)]["waiting"]:
                return await ctx.send(embed=embeds.simple_embed(False, f'you cannot leave a team that you are not on'))
            coaches[str(coach.id)]["waiting"] = list(filter(lambda team :team != str(ctx.author.id), coaches[str(coach.id)]["waiting"]))
            coaches[str(coach.id)]["team"] = list(filter(lambda team :team != str(ctx.author.id), coaches[str(coach.id)]["team"]))
            await ctx.send(embed=embeds.simple_embed(True, f'you were removed from the team of {coach.name}'))           
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
        await update_room_permissions(ctx.guild ,coach)




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
                with open('data/coach.txt', "w") as f2:
                    f2.write(json.dumps(coaches))
        return await ctx.send(embed=embeds.dict_to_embed(parse_ids(coach)))    
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
            await ctx.send(embed=embeds.dict_to_embed(parse_ids(ctx.author)))       
        elif str(person.id) in coaches[str(ctx.author.id)]["waiting"]:
            coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != str(person.id), coaches[str(ctx.author.id)]["waiting"]))
            await ctx.send(embed=embeds.dict_to_embed(parse_ids(ctx.author)))     
        else:
            return await ctx.send(embed=embeds.simple_embed(False, f'cannot find that person in your team or waiting'))
        for person in coaches[str(ctx.author.id)]["waiting"]:
            if len(coaches[str(ctx.author.id)]["team"]) >= coaches[str(ctx.author.id)]["options"]["teamsize"]:
                break
            coaches[str(ctx.author.id)]["waiting"] = list(filter(lambda team :team != person, coaches[str(ctx.author.id)]["waiting"]))
            coaches[str(ctx.author.id)]["team"] = [*coaches[str(ctx.author.id)]["team"], person]
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
        await update_room_permissions(ctx.guild ,ctx.author)
        return await ctx.send(embed=embeds.dict_to_embed(parse_ids(ctx.author)))    

    @commands.command(
        name='move',
        description="move someone to team, waiting, or off",
        aliases=['mv'],
        usage="move eulerthedestroyer team"
    )
    async def move(self, ctx,person: PersonConverter, *, area='off' ):
        if person.id == ctx.author.id:
            return await ctx.send(embed=embeds.simple_embed(False, f'you cannot join your own team'))  
        print("the person is",person.name)
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
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
        await update_room_permissions(ctx.guild ,ctx.author)
        return await ctx.send(embed=embeds.dict_to_embed(parse_ids(ctx.author)))    

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
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
        await update_room_permissions(ctx.guild ,ctx.author)
        return await ctx.send(embed=embeds.dict_to_embed(parse_ids(ctx.author)))    



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
        with open('data/coach.txt', "w") as f:
            f.write(json.dumps(coaches))
        await update_room_permissions(ctx.guild ,ctx.author)
        return await ctx.send(embed=embeds.dict_to_embed(parse_ids(ctx.author)))    

    @commands.command(
        name='room',
        description="create a discord channel that only members of your team can see",
        aliases=['create-room',"make-room"],
        usage="room"
    )
    async def room(self, ctx):
        with open('data/coach.txt', "r") as f:
            coaches=json.loads(f.read())
            if str(ctx.author.id) not in coaches: 
                return await ctx.send(embed=embeds.simple_embed(False, f'you do not have anyone on your team. Get people to join your team before you can have a room.')) 
            if len(coaches[str(ctx.author.id)]["team"]) == 0: 
                return await ctx.send(embed=embeds.simple_embed(False, f'you have no one on your team')) 
        with open('data/rooms.txt', "r") as f1:
            rooms=json.loads(f1.read())
            if str(ctx.guild.id) in rooms:
                if str(ctx.author.id) in rooms[str(ctx.guild.id)]:
                    return await ctx.send(embed=embeds.simple_embed(False, f'you already have a room at <#{rooms[str(ctx.guild.id)][str(ctx.author.id)]}>')) 
            category = discord.utils.find(lambda m: m.name =="coaching rooms", ctx.guild.channels)
            if category is None:
                category = await ctx.guild.create_category("coaching rooms")
            created_channel = await ctx.guild.create_text_channel(name=f'{ctx.author.name}\'s-coaching-room ', category=category)
            await created_channel.set_permissions(ctx.author, send_messages=True)
            await created_channel.set_permissions(ctx.author, read_messages=True)
            #await created_channel.set_permissions(ctx.author, manage_messages=True)
            #await created_channel.set_permissions(ctx.author, manage_channel=True)
            await created_channel.set_permissions(discord.utils.find(lambda u:int(u.id) ==698691997279584338, ctx.guild.members), read_messages=True)
            await created_channel.set_permissions(discord.utils.find(lambda u:int(u.id) ==698691997279584338, ctx.guild.members), send_messages=True)
            await created_channel.set_permissions(discord.utils.find(lambda u:int(u.id) ==464954455029317633, ctx.guild.members), read_messages=True)
            await created_channel.set_permissions(discord.utils.find(lambda u:int(u.id) ==464954455029317633, ctx.guild.members), send_messages=True)
            await created_channel.set_permissions(self.bot.user, send_messages=True)
            await created_channel.set_permissions(self.bot.user, read_messages=True) 
            await created_channel.set_permissions(ctx.guild.default_role, send_messages=False)

            await ctx.send(embed=embeds.simple_embed(True, f'the room was succesfully created at <#{created_channel.id}>'))
            await created_channel.send(embed=embeds.simple_embed(True, f'this is a coaching room, which means that whenever someone joins or leaves this team,he will automatically be added to this channel'))

            if str(ctx.guild.id) not in rooms:
                rooms[str(ctx.guild.id)] = {}
            rooms[str(ctx.guild.id)][str(ctx.author.id)] = str(created_channel.id)
        with open('data/rooms.txt', "w") as f2:
            f2.write(json.dumps(rooms))
        await update_room_permissions(ctx.guild ,ctx.author)

            
def setup(bot):
    bot.add_cog(Coach(bot))


async def update_room_permissions(guild, coach):
    print("update_room_permissions called")
    with open('data/coach.txt', "r") as f:
        #print("f.read() is",f.read())
        coaches=json.loads(f.read())
        with open('data/rooms.txt', "r") as f1:
            rooms=json.loads(f1.read())
            if str(guild.id) not in rooms:
                print("bruh ")
                return
            if str(coach.id) not in rooms[str(guild.id)]:
                print("bruh x2")
                return
            channel = discord.utils.find(lambda m: str(m.id) ==rooms[str(guild.id)][str(coach.id)], guild.channels)
            if channel is None:
                print("bruh x3")
                return
            for person in channel.members:
                if person.id == coach.id:
                    continue
                elif int(person.id) == 698691997279584338 or int(person.id) ==464954455029317633:
                    await channel.set_permissions(person, read_messages=True)
                    await channel.set_permissions(person, send_messages=True)
                    continue
                elif person in  coaches[str(coach.id)]["team"]:
                    continue
                else:
                    try:
                        print("trying to deny",person.name,"access")
                        await channel.set_permissions(person, read_messages=True)
                        await channel.set_permissions(person, send_messages=False)
                    except:
                        pass
            for person in coaches[str(coach.id)]["team"]:
                found_person = discord.utils.find(lambda m: str(m.id) == person, guild.members)
                print("trying to allow",found_person.name,"into the room")
                #try:
                await channel.set_permissions(found_person, read_messages=True)
                await channel.set_permissions(found_person, send_messages=True)
                #except:
                #    pass
            
            
            
