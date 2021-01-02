import json
from hashlib import sha1
import os
import requests
import base64

auth_code=os.environ.get('AUTH_CODE')
authTstamp="1609519786"
auth_user_id = "19999486"

async def make_con_api_request(action, **kwargs):
    url_string = "&".join(list(map(lambda x: f'{x[0]}={x[1]}', kwargs.items())))
    hash_code=sha1(f'uberCon{action}{url_string}&authTstamp={authTstamp}&authUserID={auth_user_id}{auth_code}'.encode('utf-8')).hexdigest()
    url = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action={action}&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'{url_string}&authTstamp={authTstamp}&authUserID={auth_user_id}'.encode('ascii'))
    }
    r = requests.post(url, data)
    r.encoding = "utf-8"
    result = r.json()
    return result

    ##{"requestID":7,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":8903,"version":78,"autoPolling":true,"stateIDs":{"1":"214614529","2":"154030604663574583","3":"2199854588340","4":"-1303479959","5":"-1424254260249347878","6":"-31990256649","7":"32","11":"-1596266382","12":"-1578923503","13":"533","14":"-1838379474","15":"0","16":"7795040645521","19":"60","23":"1609637749","24":"1609616335851","25":"-1619996831","28":"1","@c":"java.util.HashMap"},"tstamps":{"3":"1609616565803","6":"1609616565803","@c":"java.util.HashMap"},"tstamp":"1609616561","client":"con-client","hash":"2908b3aaaf3eddeba80b35f2a3dd9aa220b6f1a8","sessionTstamp":0,"gameID":"3657030","playerID":29,"siteUserID":"19999486","adminLevel":null,"rights":"chat","userAuth":"ac6de37f35ceda392ad979b2ca0efba160d212bd"}: 
async def in_game_req(request_id:int,game_number:int, options={}):
    congs_number= "https://congs1.supremacy1914.com/"
    dataJson={"requestID":+request_id,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":True,"option":None,"actions":None,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":str(game_number),"playerID":"0","siteUserID":"0","adminLevel":None,"rights":"chat","userAuth":"0"}
    dataJson.update(options)
    data = json.dumps(dataJson)+":"
    print("data is",data)
    r = requests.post(congs_number, data)
    r.encoding = 'utf-8' 
    result =  r.json()
    try:
        congs_number= result["result"]["detailMessage"]
        # data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
        new_url =f'https://{congs_number}/'
        # print(new_url)
        request = requests.post(new_url, data)
        request.encoding = 'utf-8' 
        result =request.json() 
    except Exception as e:
        # print("e is",e)
        pass
    # print("result is", result)
    try:
        result=result["result"]["states"]
    except:
        print("result", result)
        raise Exception("bruh in_game req failed")

    # print("going to return", result)
    return result
async def game_news(game_number:int):
    req = await in_game_req(7, game_number,{
        "stateIDs":{},
        "autoPolling": True,
    })
    return req
async def request_game(game_number:int):
    req = await in_game_req(0, game_number)
    return req["1"]
    # congs_number= "https://congs1.supremacy1914.com/"
    # data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
    # r = requests.post(congs_number, data)
    # r.encoding = 'utf-8' 
    # result =  r.json()
    # try:
    #     congs_number= result["result"]["detailMessage"]
    #     data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
    #     new_url =f'https://{congs_number}/'
    #     # print(new_url)
    #     request = requests.post(new_url, data)
    #     request.encoding = 'utf-8' 
    #     result =request.json() 
    # except Exception as e:
    #     # print("e is",e)
    #     pass
    # # print("result is", result)
    # result=result["result"]["states"]["1"]
    # return result

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