import discord; import re; import asyncio
from redbot.core import commands
from .pcx_lib import type_message
from .split import split_into_sentences
client = commands.Bot(command_prefix = '.')
# example url
# https://lmgtfy.app/?q=fuck+this+nonsense%3F

#Redbot cog that takes the above message and converts it to a "lmgtfy" link.
class lmgtfy(commands.Cog):
    @commands.command()
    @staticmethod
    async def google(self, ctx: commands.Context):
        #Convert the above message into lmgtfy link
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        sentence = split_into_sentences(message)
        for i in sentence:
            if '?' in i[::-1]:
                o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', i)
                output = "https://lmgtfy.app/?q="
                for l in o:
                    output = ''.join([output, l+'+'])
                return output[:-1] + '?'
            elif '?' not in i[::-1]:
                continue
            else:
                return "I can't seem to find a question."
