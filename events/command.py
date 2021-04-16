async def command(bot,ctx):
    # print(bot, ctx)
    try:
        bot.commands_responded+=1
    except:
        bot.commands_responde=1