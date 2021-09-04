import discord; import re
from redbot.core import commands
from .split import split_into_sentences

class lmgtfy(commands.Cog):
    """Redbot cog that takes a message and makes a 'lmgtfy' link out of it."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lmgtfy(self, ctx: commands.Context):
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        try:
            for i in split_into_sentences(message):
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
        except:
            await ctx.send("I can't make sense of this. Try harder.")