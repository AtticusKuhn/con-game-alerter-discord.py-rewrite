from discord.ext import commands
import methods

class FormatConverter(commands.Converter):
    async def convert(self, ctx, *format):
        print("input was", format)
        format= " ".join(format)
        parsed_format=methods.parse_format(format)
        print("parsed format is",parsed_format )
        if not parsed_format:
            raise Exception("not a valid format")
        format = parsed_format
        print("format converter returns", format)
        return format
