import threading
import sqlite3
import asyncio
from scraper.request_game import get_global_games
from time import time
from data.config import CONFIG
import nest_asyncio
import discord_utils.embeds as embeds
from datetime import datetime
#from task import Task
##def start_loop(client):
##    asyncio.run(infinite_loop(client))
#
#async def infinite_loop(client):
#    print('infinite_loop called')
#    await asyncio.sleep(10)
#    await check_for_alerts(client)
#def asyncio_run(future, as_task=True):
#    """
#    A better implementation of `asyncio.run`.
#
#    :param future: A future or task or call of an async method.
#    :param as_task: Forces the future to be scheduled as task (needed for e.g. aiohttp).
#    """
#    try:
#        loop = asyncio.get_running_loop()
#    except RuntimeError:  # no event loop running:
#        loop = asyncio.new_event_loop()
#        return loop.run_until_complete(_to_task(future, as_task, loop))
#    else:
#        nest_asyncio.apply(loop)
#        return asyncio.run(_to_task(future, as_task, loop))
#
#
#def _to_task(future, as_task, loop):
#    if not as_task: #or isinstance(future, Task):
#        return future
#    return loop.create_task(future)


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
        print("alertpeople is ", alertpeople)
        format = game["properties"]["title"]
        id= game["properties"]["gameID"]
        game = game["properties"]
        #print('alert people called')
        #conn = sqlite3.connect('data/database.db',isolation_level=None)
        #c = conn.cursor()
        ##print("format is ", format)
        #c.execute('SELECT * FROM alertpeople WHERE format=? OR format="all"', (format,))
        #people= c.fetchmany()
        #c.execute('SELECT * FROM alertpeople')
        #test = c.fetchmany()
        #print("test is ",test)
        #print("people are ", people)
        people = [person for person in alertpeople if person.split(" ")[1]==format or person.split(" ")[1]=="all" ]
        for person in people:
            person=person.split(" ")[0]
            user = client.get_user(int(person))
            print("sending...")
            await user.send(embed=embeds.simple_embed(True,f'Game {id} has just started at time {datetime.utcfromtimestamp(int(game["startofgame2"])).strftime("%Y-%m-%d %H:%M:%S")}. It is at {int(game["nrofplayers"])-int(game["openSlots"])}/{game["nrofplayers"]} You can join it by going to https://www.conflictnations.com/play.php?bust=1&gameID={id}'))
        #conn.close()

async def check_for_alerts(client):
    #print("check for alerts called")
    seengames=[]
    with open('data/seengames.txt', "r") as f:
        seengames=f.read().split("\n")
        print("seengames is", seengames)
        #conn = sqlite3.connect('data/database.db')
        #c = conn.cursor()
        #c1 = conn.cursor()
        result = await get_global_games()
        #print("after games have been fetched")
        games = result["result"]["games"]
        #values_to_insert=[]
        newly_seen_games=[]
        for game in games:
            if int(game["properties"]["openSlots"])>0:
                has_seen=[seengame for seengame in seengames if seengame.startswith(str(game["properties"]["gameID"]))]
                print("has seen is", has_seen)
                if len(has_seen)==0: 
                    await alert_people(client, game)
                    seengames.append(f'{game["properties"]["gameID"]} {float(time())}')
                #values_to_insert.append((game["properties"]["gameID"],float(time()),))
        #sql_string = f'INSERT INTO seengames  VALUES {",".join(list(map(lambda x:"("+str(x[0])+","+str(x[1])+")", values_to_insert)))}'
        #print("sql_stirng", sql_string)
        #print("about to insert", inserting_value)
        #c.execute(sql_string)
        #passed_time=int(time())-int(CONFIG.delete_time)
        #print("passed time is", passed_time)
        #c.execute('DELETE FROM seengames WHERE time < ?',(
        #    passed_time,
    # ))
        #conn.commit()
        #print("rowcount",c.rowcount )
        #c1.execute('SELECT * FROM seengames')
        #seengames = c1.fetchmany()
        #print("seengames after deletion is",seengames )
        #conn.commit()
        #conn.close()
        seengames=list(filter(lambda g: float(time())- float(g.split(" ")[len(g.split(" "))-1]) < CONFIG.delete_time if g !='' else True  ,seengames))

    with open('data/seengames.txt', "w") as f:
        print("at the end, seengames is ", seengames)
        f.write("\n".join(list(set(seengames))))
        return check_for_alerts


    


