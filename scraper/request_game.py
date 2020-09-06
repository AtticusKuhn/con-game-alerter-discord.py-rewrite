import json
import asyncio
from hashlib import sha1
import os
import urllib
import requests
import base64
auth_code=os.environ.get('AUTH_CODE')
auth_code_2=os.environ.get('AUTH_CODE_2')
authTstamp="1599322837"

async def request_game(game_number:int):
    congs_number= "https://congs6.c.bytro.com/"
    data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
    print(1)
    result = json.loads(requests.post(congs_number, data).text)
    print(2)
    try:
        congs_number= result["result"]["detailMessage"]
        data='{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'+str(game_number)+'","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:'
        print(3)
        result = json.loads(requests.post(f'https://{congs_number}/', data).text)["result"]["states"]["1"]
        print(4)
    except:
        result=result["result"]["states"]["1"]
    return result

async def get_player_ranking(player_name):
    hash_code=sha1(f'uberConsearchUserusername={player_name}&authTstamp={authTstamp}&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    url = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=searchUser&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'username={player_name}&authTstamp={authTstamp}&authUserID=19999486'.encode('ascii'))
    }
    result = requests.post(url, data).text
    json_parsed_result = json.loads(result)
    if len(json_parsed_result["result"])==0:
        return False
    player = json_parsed_result["result"][0]
    print(player)
    hash_code2=sha1(f'uberCongetUserDetailsFireflyuserID={str(player["userID"])}&username=1&email=1&emailChangeRequest=1&referrer=1&notifications=1&inventory=1&rankProgress=1&acl=1&stats=1&awardProgress=1&subscriptions=1&links=1&unreadMessages=1&allianceInvites=1&alliance=1&allianceMemberShip=1&deletionStatus=1&locale=en&authTstamp={authTstamp}&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    url2 = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=getUserDetailsFirefly&hash={hash_code2}&outputFormat=json&apiVersion=20141208'
    data2 = {
        "data": base64.b64encode(f'userID={player["userID"]}&username=1&email=1&emailChangeRequest=1&referrer=1&notifications=1&inventory=1&rankProgress=1&acl=1&stats=1&awardProgress=1&subscriptions=1&links=1&unreadMessages=1&allianceInvites=1&alliance=1&allianceMemberShip=1&deletionStatus=1&locale=en&authTstamp={authTstamp}&authUserID=19999486'.encode('ascii'))
    }
    result2 = requests.post(url2, data2).text
    json_parsed_result2 = json.loads(result2)
    #print(json_parsed_result2)
    return json_parsed_result2

async def get_global_games():
    hash_code=sha1(f'uberCongetInternationalGamesnumEntriesPerPage=20&page=1&lang=en&isFilterSearch=false&openSlots=1&global=1&authTstamp={authTstamp}&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    url = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=getInternationalGames&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'numEntriesPerPage=20&page=1&lang=en&isFilterSearch=false&openSlots=1&global=1&authTstamp={authTstamp}&authUserID=19999486'.encode('ascii'))
    }
    result = requests.post(url, data).text
    json_parsed_result = json.loads(result)
    return json_parsed_result

async def get_alliance(alliance_name):
    hash_code=sha1(f'uberConsearchAlliancename={alliance_name}&authTstamp={authTstamp}&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    url_parsed=urllib.parse.quote(alliance_name)
    url = f'https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=searchAlliance&hash={hash_code}&outputFormat=json&apiVersion=20141208'
    data = {
        "data": base64.b64encode(f'name={url_parsed}&authTstamp={authTstamp}&authUserID=19999486'.encode('ascii'))
    }
    result = requests.post(url, data).text
    json_parsed_result = json.loads(result)
    alliance = json_parsed_result["result"]
    print(alliance)
    return alliance

