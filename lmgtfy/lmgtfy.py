import discord; import re
from redbot.core import commands
from .split import split_into_sentences

class lmgtfy(commands.Cog):
    """Redbot cog that takes a message and makes a 'lmgtfy' link out of it."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lmgtfy(self, ctx, Question):
        sentence = split_into_sentences(ctx)
        for i in sentence:
            if '?' in i[::-1]:
                o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', i)
                output = "https://lmgtfy.app/?q="
                for l in o:
                    output = ''.join([output, l+'+'])
                output = output[:-1] + '?'
                await ctx.send(output)
            elif '?' not in i[::-1]:
                continue
            else:
                await ctx.send("I can't seem to find a question.")