from discord.ext import commands
import json

import discord_utils.embeds as embeds
from methods import seconds_to_time, parse_costs

class Simulator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='damage_calculator',
        description='get info on how an exchange would go',
        aliases=['calc'],
        usage="calc"
    )
    async def calc(self, ctx,):
        stack1 = []
        stack2=[]
        stopped = False
        await ctx.send(embed=embeds.simple_embed(True,
            '''to add a unit to a stack, type `{stack number} {level} {quantity} {unit}`. 
For example, you could type `1 2 3 motorized infantry` or `2 3 1 heavy bomber`. Then,
when you are done, type `end` and to simuate an attack between the 2 stacks.
            '''
            ))
        with open('data/units.json') as json_file:
            units = json.load(json_file)
            while not stopped:
                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author
                response = await self.bot.wait_for('message', check=check)
                if response.content == "end":
                    stopped = True
                    break
                resp_array = response.content.split(" ")
                stack_number = int(resp_array[0])
                level = int(resp_array[1])
                quantity = int(resp_array[2])
                unit_name = " " .join(resp_array[3:])
                found_units = list(filter(lambda unit:unit["unitName"].lower()==unit_name.lower(), units))
                ##errors
                if len(found_units)==0:
                    return await ctx.send(embed=embeds.simple_embed(False,"cannot find unit"))
                if len(found_units) < level:
                    return await ctx.send(embed=embeds.simple_embed(False,"unit does not exist at that level"))
                unit = {
                    "unit":found_units[level],
                    "quantity":quantity,
                    "health":int(found_units[level]["hitPoints"])*quantity
                }
                if stack_number == 1:
                    stack1.append(unit)
                else:
                    stack2.append(unit)
                await ctx.send("ok recieved that unit")
        #print("at the end,stack1 is , ",stack1)
        #print("at the end,stack2 is , ",stack2)
        await ctx.send("calculating attacks....")
        for attacking_unit in stack1:
            for defending_unit in stack2:
                found_offensive_value = 0
                #try:
                for offensive_value in attacking_unit["unit"]["strength"].split(","):
                    if offensive_value.split("=")[0] == "a"+defending_unit["unit"]["unitClass"]:
                        found_offensive_value =  offensive_value.split("=")[1]
                        break
                found_defensive_value = 0
                for defensive_value in defending_unit["unit"]["defence"].split(","):
                    if defensive_value.split("=")[0] == "a"+attacking_unit["unit"]["unitClass"]:
                        found_defensive_value =  defensive_value.split("=")[1]
                        break
                attacking_unit["health"] -=int(found_defensive_value)*quantity
                ##print("before the error,defending_unit is " ,defending_unit)
                defending_unit["health"] -=int(found_offensive_value)*quantity
                if attacking_unit["health"] <=0:
                    stack1.remove(attacking_unit)
                if defending_unit["health"] <=0:
                    stack2.remove(defending_unit)
        nice_stack1=    "\n".join(list(map(lambda x:f'{x["unit"]["unitName"]} {x["health"]}', stack1)))            
        nice_stack2=    "\n".join(list(map(lambda x:f'{x["unit"]["unitName"]} {x["health"]}', stack2)))
        return await ctx.send(embed=embeds.dict_to_embed({
            "attacking stack":nice_stack1,
            "defending stack":nice_stack2
        }))            

                
               # except:
               #     offensive_value = 0
                



def setup(bot):
    bot.add_cog(Simulator(bot))