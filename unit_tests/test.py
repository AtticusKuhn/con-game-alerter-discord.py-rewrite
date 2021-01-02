
import bruh.ext.test as dpytest
from make_bot import make_bot
from termcolor import colored
from unit_tests.generate_tests import tests

async def run_tests():
    # return
    bot = await make_bot()
    dpytest.configure(bot)
    results =[await test.run()  for test in tests]
    failures = list(filter( lambda test: not test.success, results))
    if len(failures) == 0:
        print(colored(f'all tests passed {len(results)}/{len(results)}', "green"))
        return f'🟢 all tests passed {len(results)}/{len(results)}'
    else:
        parsed_failures = "\n".join(list(map(lambda failure: f' {failure.name} failed-  {failure.comment}', failures)))
        print(colored(parsed_failures,"red"))
        return  f'🔴 {parsed_failures}'
