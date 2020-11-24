import re
async def message(bot,message):
    message.flags = re.findall(r'\-[^\s]*', message.content)
    message.content = re.sub(r'\-[^\s]*', "", message.content)
    await bot.process_commands(message)
