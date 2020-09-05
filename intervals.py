import threading
import sqlite3
import asyncio
from scraper.request_game import get_global_games
from time import time
from data.config import CONFIG
import nest_asyncio
import discord_utils.embeds as embeds
from datetime import datetime


async def set_interval(func, sec, *args):
    #print("set_interval called")
    async def func_wrapper():
        #print('func_wrapper called')
        await asyncio.sleep(10)
        await func(*args)

        await set_interval(func, sec,*args)
        return func_wrapper
    def async_workaround():
        #print("async_workaround called")
        asyncio.run(func_wrapper())
        #loop = asyncio.new_event_loop()
        #loop.call_soon_threadsafe(func_wrapper)<- when I do this func_wrapper is not called
        #asyncio_run(func_wrapper())<- this results in an error and idk why
    t = threading.Timer(sec, await func_wrapper() )
    t.start()
    return t

async def alert_people(client, game):
    with open('data/alertpeople.txt', "r") as f:
        alertpeople=f.read().split("\n")
        #print("alertpeople is ", alertpeople)
        format = game["properties"]["title"]
        id= game["properties"]["gameID"]
        game = game["properties"]
        people = [person for person in alertpeople if " ".join(person.split(" ")[1:])==format or person.split(" ")[len(person.split(" "))-1]=="all" ]
        for person in people:
            person=person.split(" ")[0]
            try:
                user = client.get_user(int(person))
                print("sending... to", user.name)
                await user.send(embed=embeds.simple_embed(True,f'Game {id} {format} has just started at time {datetime.utcfromtimestamp(int(game["startofgame2"])).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]} You can join it by going to https://www.conflictnations.com/play.php?bust=1&gameID={id}'))
            except:
                print("oof cannot send to",user.name )

async def check_for_alerts(client):
    #print("check for alerts called")
    seengames=[]
    with open('data/seengames.txt', "r") as f:
        seengames=f.read().split("\n")
        #print("seengames is", seengames)
        result = await get_global_games()
        games = result["result"]["games"]
        newly_seen_games=[]
        for game in games:
            if int(game["properties"]["openSlots"])>0:
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


    


