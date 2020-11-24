import threading
import asyncio
from api.con_api import get_global_games
from time import time
from data.config import CONFIG
import discord_utils.embeds as embeds
from datetime import datetime
import json

async def set_interval(func, sec, *args):
    async def func_wrapper():
        await asyncio.sleep(10)
        await func(*args)
        await set_interval(func, sec,*args)
        return func_wrapper
    def async_workaround():
        asyncio.run(func_wrapper())
    t = threading.Timer(sec, await func_wrapper() )
    t.start()
    return t

async def alert_people(client, game):
    with open('data/alertpeople2.txt', "r") as f:
        alertpeople=json.loads(f.read())#f.read().split("\n")
        format = game["properties"]["title"]
        id= game["properties"]["gameID"]
        game = game["properties"]
        for person in alertpeople.copy():
            if alertpeople[person]["format"]==format or alertpeople[person]["format"]=="all":
                try:
                    user = client.get_user(int(person))
                    # client.print("sending... to"+ user.name)
                    await user.send(embed=embeds.simple_embed(True,f'Game {id} {format} has just started at time {datetime.utcfromtimestamp(int(game["startofgame2"])).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]} You can join it by going to https://www.conflictnations.com/play.php?bust=1&gameID={id}'))
                except:
                    client.print("oof cannot send to" )
                    del alertpeople[person]
                    break
                if "uses" in alertpeople[person]:
                    print("uses is in person")
                    alertpeople[person]["uses"]-=1
                    if alertpeople[person]["uses"]<=0:
                        del alertpeople[person]
                        continue
            if "time" in alertpeople[person]:
                print("time is in person")
                if time() > float(alertpeople[person]["time"]):
                    del alertpeople[person]
                    continue
    with open('data/alertpeople2.txt', "w") as f:
        f.write(json.dumps(alertpeople))


async def check_for_alerts(client):
    #print("check for alerts called")
    seengames=[]
    with open('data/seengames.txt', "r") as f:
        seengames=f.read().split("\n")
        #print("seengames is", seengames)
        result = await get_global_games()
        #print('result',result)
        games = result["result"]["games"]
        newly_seen_games=[]
        for game in games:
            if int(game["properties"]["openSlots"])>20:
                has_seen=[seengame for seengame in seengames if seengame.startswith(str(game["properties"]["gameID"]))]
                #print("has seen is", has_seen)
                if len(has_seen)==0: 
                    await alert_people(client, game)
                    seengames.append(f'{game["properties"]["gameID"]} {float(time())}')
        seengames=list(filter(lambda g: float(time())- float(g.split(" ")[len(g.split(" "))-1]) < CONFIG.delete_time if g !='' else True  ,seengames))
    with open('data/seengames.txt', "w") as f:
        #print("at the end, seengames is ", seengames)
        f.write("\n".join(list(set(seengames))))
        return check_for_alerts


    


