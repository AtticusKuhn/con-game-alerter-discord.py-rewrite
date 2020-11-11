from unit_tests.test_methods import Test
#import bruh as dpytest

async def help_test_run(dpytest):
    print(1)
    await dpytest.message("!con help")
    print(2)
    help_embed = dpytest.get_message()
    return {"success":help_embed is not None,"comment":help_embed}
help_test = Test(
    name="help test",
    run=help_test_run
)

tests = [
    help_test
]