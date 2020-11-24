import json
#import asyncio
from hashlib import sha1
import os
import urllib
import requests
import base64
auth_code=os.environ.get('AUTH_CODE')
authTstamp="1605630054"
auth_user_id = "19999486"

async def make_con_api_request(action, **kwargs):
    url_string = "&".join(list(map(lambda x: f'{x[0]}={x[1]}', kwargs.items())))
    # print("url_string", url_string)
    hash_code=sha1(f'uberCon{action}{url_string}&authTstamp={authTstamp}&authUserID={auth_user_id}{auth_code}'.encode('utf-8')).hexdigest()
    url = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action={action}&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'{url_string}&authTstamp={authTstamp}&authUserID={auth_user_id}'.encode('ascii'))
    }
    result = requests.post(url, data).json()
    return result
async def request_game(game_number:int):
    congs_number= "https://congs1.supremacy1914.com/"
    data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
    r = requests.post(congs_number, data)
    r.encoding = 'utf-8' 
    result =  r.json()
    try:
        congs_number= result["result"]["detailMessage"]
        data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
        new_url =f'https://{congs_number}/'
        print(new_url)
        request = requests.post(new_url, data, stream=True)
        request.encoding = 'utf-8' 
        result =r.json() 
    except:
        pass
    result=result["result"]["states"]["1"]
    return result

async def get_player_ranking(player_name):
    result = await make_con_api_request("searchUser",
        username=player_name
    )
    if len(result["result"])==0:
        return False
    player = result["result"][0]
    result2 = await make_con_api_request("getUserDetailsFirefly",
        userID=player["userID"],
        username=1,
        email=1,
        emailChangeRequest=1,
        referrer=1,
        notifications=1,
        inventory=1,
        rankProgress=1,
        acl=1,
        stats=1,
        awardProgress=1,
        subscriptions=1,
        links=1,
        unreadMessages=1,
        allianceInvites=1,
        alliance=1,
        allianceMemberShip=1,
        deletionStatus=1,
        locale="en"
    )
    return result2

async def get_global_games():
    numbers = "1000"
    # result = await make_con_api_request("getInternationalGames",
    #     numEntriesPerPage=numbers,
    #     page=1,
    #     lang="en",
    #     isFilterSearch="false",
    #     openSlots=1,
    #     global=1
    # )
    hash_code=sha1(f'uberCongetInternationalGamesnumEntriesPerPage={numbers}&page=1&lang=en&isFilterSearch=false&openSlots=1&global=1&authTstamp={authTstamp}&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    url = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=getInternationalGames&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'numEntriesPerPage={numbers}&page=1&lang=en&isFilterSearch=false&openSlots=1&global=1&authTstamp={authTstamp}&authUserID=19999486'.encode('ascii'))
    }
    result = requests.post(url, data).text
    # print("global games result is", result)
    json_parsed_result = json.loads(result)
    if  "games" not  in json_parsed_result["result"]:
        print("error!!!!", result)
    return json_parsed_result

async def get_alliance(alliance_name):
    json_parsed_result = await make_con_api_request("searchAlliance",
        name=alliance_name,
    )
    alliance = json_parsed_result["result"]
    return alliance 
async def get_players_in_game(game_id:int):
    return await make_con_api_request("getGame",
        gameID=game_id
    )
def get_session():
    print("get_session called")
    hash_code=sha1(f'authTstamp={authTstamp}&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    url = f' https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=getSessionToken&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'authTstamp={authTstamp}&authUserID=19999486'.encode('ascii'))
    }   
    print("url", url)
    print("data", data)
    result =json.loads(requests.post(url, data).text)
    print("result", result)
    return result