import discord
import re
from redbot.core import commands
from .split import split_into_sentences
#v0.2.0
class lmgtfy(commands.Cog):
    """
    Redbot cog that takes a message and makes a 'lmgtfy' link out of it.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx: commands.Context):
        """
        Creates a 'lmgtfy' link from a previous question
        """
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        if not message:
            await ctx.send("I can't seem to find a question!")
        for i in split_into_sentences(message):
            if 'app/?' not in i:
                if 'q=' not in i[0:2]:
                    if '?' in i[::-1]:
                        o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', i)
                        output = "https://lmgtfy.app/?q="
                        for l in o:
                            output = ''.join([output, l+'+'])
                        output = output[:-1]
                        await ctx.send(output)
            else:
                await ctx.send("I can't seem to find a question!")

    @commands.command()
    async def lmgtfy(self, ctx: commands.Context, question):
        """
        Wrap your <question> in **double quotes**
        """
        o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', question)
        output = "https://www.google.com/search?q="
        if len(o) > 1:
            for l in o:
                output = ''.join([output, l+'+'])
            output = output[:-1]
            await ctx.send(output)
        elif len(o) == 1:
            output = ''.join([output, o])
            await ctx.send(output)
        else:
            await ctx.send("Wrap your <question> in **double quotes**")
