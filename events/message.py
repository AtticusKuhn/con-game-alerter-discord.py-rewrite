import re
async def message(bot,message):
    named_flag_regex = r'[^A-Za-z]\-\-([^\s]+)\s["\']([^"\']*)["\']'
    unnamed_flag_regex = r'[^A-Za-z]\-[^\s]*'
    message.flags = {"named":{},"unnamed":[]}
    for flag in re.findall(named_flag_regex, message.content):
        # print("flag", flag)
        message.flags["named"][flag[0]]=flag[1]
    message.content = re.sub(named_flag_regex, "", message.content)
    message.flags["unnamed"] = re.findall(r'[^A-Za-z]\-[^\s]*', message.content)
    message.content = re.sub(unnamed_flag_regex, "", message.content)
    # print(message.content)

    e = await bot.process_commands(message)
    # ctx = await bot.get_context(message)
    # cmd = ctx.command
    # if cmd is not None:
        # ans = await cmd(ctx, *ctx.args)
        # print(ans)
    if e is not None:
        print(e, "is e")
    # c = await bot.get_context(message)
    # # print("c is", c)
    # attrs = vars(c)
    # print(', '.join("%s: %s" % item for item in attrs.items()))
    # e = await bot.invoke(c)
    # print("e is ",e)
