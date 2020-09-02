from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread
#import time
import json
import asyncio
from hashlib import sha1
import os
auth_code=os.environ.get('AUTH_CODE')

async def request_game(game_number:int):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.duckduckgo.com")
    #await asyncio.sleep(4)
    congs_number= "congs4.c.bytro.com"
    execute_string = '''
        const done = arguments[0]
        $.ajax({
            type: "POST",
            url: "https://'''+congs_number+ '''/",
            data: `{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'''+str(game_number)+ '''","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:`,
            success: function( response ) {
                 "help"
                try{
                    done(JSON.stringify(JSON.parse(response).result.states["1"]))
                }catch{
                   done(response)
                }
            }
        });
    '''
    result =  json.loads(driver.execute_async_script(execute_string))
    print("result is", result)
    #await asyncio.sleep(2)
    try:
        print("in the try")
        new_congs_number = result["result"]["detailMessage"]
        print(37)
        new_execute_string = '''
        const done = arguments[0]
        $.ajax({
            type: "POST",
            url: "https://'''+new_congs_number+ '''/",
            data: `{"requestID":0,"@c":"ultshared.action.UltUpdateGameStateAction","stateType":0,"stateID":"0","addStateIDsOnSent":true,"option":null,"actions":null,"lastCallDuration":0,"version":0,"tstamp":"0","client":"con-client","hash":"0","sessionTstamp":0,"gameID":"'''+str(game_number)+ '''","playerID":"0","siteUserID":"0","adminLevel":null,"rights":"chat","userAuth":"0"}:`,
            success: function( response ) {
                try{
                    done(JSON.stringify(JSON.parse(response).result.states["1"]))
                }catch{
                    done(response)
                }
            }
        });
        '''
        data = json.loads(driver.execute_async_script(new_execute_string))
    except:
        data = result
    return data
    driver.quit()
async def get_player_ranking(player_name):
    print("get_player_ranking called")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.duckduckgo.com")
    hash_code=sha1(f'uberConsearchUserusername={player_name}&authTstamp=1598803665&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    print("the hash is", hash_code)
    execute_string = '''
        function post(path, params, method='post') {
            const form = document.createElement('form');
            form.method = method;
            form.action = path;
            for (const key in params) {
                if (params.hasOwnProperty(key)) {
                const hiddenField = document.createElement('input');
                hiddenField.type = 'hidden';
                hiddenField.name = key;
                hiddenField.value = params[key];
                form.appendChild(hiddenField);
                }
            }
                document.body.appendChild(form);
                form.submit();
        }
        post("https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=searchUser&hash='''+hash_code+ '''&outputFormat=json&apiVersion=20141208",{data:btoa("username='''+player_name+'''&authTstamp=1598803665&authUserID=19999486")})
    '''
    print("execute_string is", execute_string)
    driver.execute_script(execute_string)
    await asyncio.sleep(1)
    players =  json.loads(driver.find_elements_by_css_selector('pre')[0].text)
    player = players["result"][0]
    hash_code=sha1(f'uberCongetUserDetailsFireflyuserID={str(player["userID"])}&username=1&email=1&emailChangeRequest=1&referrer=1&notifications=1&inventory=1&rankProgress=1&acl=1&stats=1&awardProgress=1&subscriptions=1&links=1&unreadMessages=1&allianceInvites=1&alliance=1&allianceMemberShip=1&deletionStatus=1&locale=en&authTstamp=1598803665&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    print("the hash is", hash_code)
    execute_string = '''
        function post(path, params, method='post') {
            const form = document.createElement('form');
            form.method = method;
            form.action = path;
            for (const key in params) {
                if (params.hasOwnProperty(key)) {
                const hiddenField = document.createElement('input');
                hiddenField.type = 'hidden';
                hiddenField.name = key;
                hiddenField.value = params[key];
                form.appendChild(hiddenField);
                }
            }
                document.body.appendChild(form);
                form.submit();
        }
        post("https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=getUserDetailsFirefly&hash=''' +hash_code+'''&outputFormat=json&apiVersion=20141208",{data:btoa("userID='''+player["userID"]+'''&username=1&email=1&emailChangeRequest=1&referrer=1&notifications=1&inventory=1&rankProgress=1&acl=1&stats=1&awardProgress=1&subscriptions=1&links=1&unreadMessages=1&allianceInvites=1&alliance=1&allianceMemberShip=1&deletionStatus=1&locale=en&authTstamp=1598803665&authUserID=19999486")})
    '''
    print("execute_string is", execute_string)
    driver.execute_script(execute_string)
    data =  json.loads(driver.find_elements_by_css_selector('pre')[0].text)
    print("data",data)
    return data

async def get_global_games():
    print("get_global_games called")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.duckduckgo.com")
    hash_code=sha1(f'uberCongetInternationalGamesnumEntriesPerPage=10&page=1&lang=en&isFilterSearch=false&openSlots=1&global=1&authTstamp=1598803665&authUserID=19999486{auth_code}'.encode('utf-8')).hexdigest()
    #print("the hash is", hash_code)
    execute_string = '''
        function post(path, params, method='post') {
            const form = document.createElement('form');
            form.method = method;
            form.action = path;
            for (const key in params) {
                if (params.hasOwnProperty(key)) {
                const hiddenField = document.createElement('input');
                hiddenField.type = 'hidden';
                hiddenField.name = key;
                hiddenField.value = params[key];
                form.appendChild(hiddenField);
                }
            }
                document.body.appendChild(form);
                form.submit();
        }
        post("https://www.conflictnations.com/index.php?eID=api&key=uberCon&action=getInternationalGames&hash='''+hash_code+'''&outputFormat=json&apiVersion=20141208",{data:btoa("numEntriesPerPage=10&page=1&lang=en&isFilterSearch=false&openSlots=1&global=1&authTstamp=1598803665&authUserID=19999486")})
    '''
    #print("execute_string is", execute_string)
    driver.execute_script(execute_string)
    games =  json.loads(driver.find_elements_by_css_selector('pre')[0].text)
    driver.quit()
    return games

   