from unit_tests.test_methods import Test
#import bruh as dpytest
from data.config import CONFIG
import bruh.ext.test as dpytest
async def help_test_run():
    await dpytest.message(f'{CONFIG.prefix}help')
    help_embed = dpytest.get_message()
    # return {"success":False}
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
tests = [
    help_test,
    admin_test
]