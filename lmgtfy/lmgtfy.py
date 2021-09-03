import discord
import re
from redbot.core import commands
from .pcx_lib import type_message
from .split import split_into_sentences

#Redbot cog that takes the above message and converts it to a "lmgtfy" link.
class lmgtfy(commands.Cog):
    @commands.command()
    async def lmgtfy(self, ctx: commands.Context):
        #Define the command for redbot
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        if not message:
            message = "I can't translate that!"
        await type_message(
            ctx.channel,
            self.lmgtfy(message),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False),
        )
    @staticmethod
    def lmgtfy(x):
        #Convert the above message into lmgtfy link
        x = split_into_sentences(x)
        for i in x:
            if '?' in i[::-1]:
                return i
            else:
                continue