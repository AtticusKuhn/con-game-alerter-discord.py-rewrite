
import bruh.ext.test as dpytest
from make_bot import make_bot_2
from termcolor import colored
from unit_tests.generate_tests import tests

async def run_tests():
    bot = await make_bot_2()
    dpytest.configure(bot)
    results =[await test.run()  for test in tests]
    failures = list(filter( lambda test: not test.success, results))
    if len(failures) == 0:
        print(colored("all tests passed", "green"))
    else:
        parsed_failures = list(map(lambda failure: f' {failure.name} failed', failures))
        print(colored("\n".join(parsed_failures),"red"))
