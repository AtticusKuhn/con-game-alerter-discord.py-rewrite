from unit_tests.test_methods import Test
from data.config import CONFIG
import bruh.ext.test as dpytest
async def help_test_run():
    await dpytest.message(f'{CONFIG.prefix}help')
    help_embed = dpytest.get_message()
    return {"success":help_embed is not None,"comment":help_embed}
help_test = Test(
    name="does help return an embed?",
    run=help_test_run
)
async def admin():
    await dpytest.message(f'{CONFIG.prefix}exec bruh')
    admin_embed=  dpytest.get_embed()
    return{
        "success": admin_embed.description=="only eulerthedestroyer#2074 can use admin commands",
        "comment":admin_embed 
    }   
admin_test = Test(
    name="are admin commands denied to non-admins?",
    run=admin
)
from api.con_api import get_global_games
async def global_games():
    games=  await get_global_games()
    return{
        "success": "games"  in games["result"],
        "comment":games
    }
global_games_test = Test(
    name="does get_global_games work?",
    run=global_games
)
async def command_player():
    await dpytest.message(f'{CONFIG.prefix}pl rulebrit')
    player_embed = dpytest.get_embed()
    # print(player_embed.color, type(player_embed.color))
    return {
        "success":str(player_embed.color) == "#00ff00",
        "comment":player_embed
    }
command_player_test = Test(
    name="does player command return a player?",
    run=command_player
)
async def previous():
    await dpytest.message(f'{CONFIG.prefix}help')
    await dpytest.message(f'{CONFIG.prefix}previous')
    pre_embed = dpytest.get_embed()
    return {
        "success": pre_embed is not None and str(pre_embed.color) == "#00ff00",
        "comment":pre_embed
    }
pre_test = Test(
    name="does the previous command (repeat previously said command) work?",
    run=previous
)
from api.con_api import request_game
async def req_game():
    some_random_game_id = (await get_global_games())["result"]["games"][0]["properties"]["gameID"]
    game = await request_game(some_random_game_id)
    return {
        "success":True,
        "comment":game
    }
req_game_test = Test(
    name="does requesting the data of a specific game work?",
    run=req_game
)

tests = [
    help_test,
    admin_test,
    global_games_test,
    command_player_test,
    pre_test,
    req_game_test
]