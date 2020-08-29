from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from threading import Thread
#import time
import json
import asyncio

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
