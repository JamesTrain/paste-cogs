import discord; import re; import asyncio
from redbot.core import commands
from .pcx_lib import type_message
from .split import split_into_sentences

# example url
# https://lmgtfy.app/?q=fuck+this+nonsense%3F

#Redbot cog that takes the above message and converts it to a "lmgtfy" link.
class lmgtfy(commands.Cog):
    @commands.command()
    async def lmgtfy(self, ctx: commands.Context):
        #Define the command for redbot
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        if not message:
            message = "I can't seem to detect any questions."
        else:
            await type_message(
                ctx.channel,
                self.google(message),
                allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False)
                ,
            )

    @staticmethod
    def google(io):
        #Convert the above message into lmgtfy link
        sentence = split_into_sentences(io)
        for i in sentence:
            if '?' in i[::-1]:
                o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', i)
                output = "https://lmgtfy.app/?q="
                for l in o:
                    output = ''.join([output, l+'+'])
                return discord.Attachment(str(output[:-1]+'?'))
            elif '?' not in i[::-1]:
                continue
            else:
                return "I can't seem to find a question."
