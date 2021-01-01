import re
async def message(bot,message):
    message.flags = re.findall(r'[^A-Za-z]\-[^\s]*', message.content)
    message.content = re.sub(r'[^A-Za-z]\-[^\s]*', "", message.content)
    await bot.process_commands(message)
