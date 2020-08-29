from discord.ext import commands
# Import the keep alive file
import keep_alive
import os
##events
from events.error import command_error
from events.ready import ready

def get_prefix(client, message):
    prefixes = ['!con ']    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
    if not message.guild:
        prefixes = ['!con']   # Only allow '==' as a prefix when in DMs
    return commands.when_mentioned_or(*prefixes)(client, message)    # Allow users to @mention the bot instead of using a prefix when using a command.
 
bot = commands.Bot(        # Create a new bot                                     
    command_prefix=get_prefix,                              # Set the prefix
    description='A bot used for conflict of nations',                  # Set a description for the bot
    owner_id=464954455029317633,                            # Your unique User ID
    case_insensitive=True                                   # Make the commands case insensitive
)

@bot.event
async def on_ready():
    await ready(bot)

@bot.event
async def on_command_error(ctx,error):
    await command_error(ctx, error)

keep_alive.keep_alive()# Start the server
token=os.environ.get('DISCORD_BOT_SECRET')
bot.run(token)# Finally, login the bot

