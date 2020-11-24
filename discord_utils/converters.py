from discord.ext import commands
import methods
import re
from Levenshtein import distance
from discord.ext.commands import BadArgument

class FormatConverter(commands.Converter):
    async def convert(self, ctx, *input_format):
        input_format= " ".join(input_format)
        parsed_format=methods.parse_format(input_format)
        print("parsed format is",parsed_format )
        if not parsed_format:
                raise BadArgument('Format "{}" not found'.format(input_format))
        input_format = parsed_format
        print("format converter returns", input_format)
        return input_format


class PersonConverter(commands.Converter):
    async def convert(self, ctx, ping):
        my_distance=1000
        current_member=""
        for member in ctx.guild.members:
            if member.name == ping:
                return member
            if len(re.findall(r'\d{18}',str(member.id)))>0:
                if re.findall(r'\d{18}',str(member.id)) ==re.findall(r'\d{18}',str(ping)):
                    return member
            if member.nick==ping:
                return member
            if member.name.startswith(ping):
                return member
            test_distance = distance(ping, member.name)
            if test_distance< my_distance:
                my_distance = test_distance
                current_member = member
        return current_member
