import asyncio
import io
import re
import time
from collections import namedtuple

import aiohttp
import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

# generate random integer values
from random import seed
from random import randint
# seed random number generator
seed(1)

BaseCog = getattr(commands, "Cog", object)

class Vibecheck(BaseCog):
    """Check them vibes"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374574)
        default_guild = {}
        self.config.register_guild(**default_guild)
        self.config.register_user(vibe=0)
        self.config.register_user(hasrun=0)

    @commands.command()
    async def vibecheck(self, ctx: commands.Context):
        """Check your vibes"""
        vibe = randint(1, 20)
        await ctx.send(":game_die: {} checked their vibe and got {}".format(
            ctx.message.author.mention,vibe)
        )
        if vibe == 1:
            await ctx.send("lmaooo")
        if vibe < 6:
            await ctx.send("Sucks for you bro")
        elif vibe < 11:
            await ctx.send("I guess that's fine")
        elif vibe < 16:
            await ctx.send("Pretty sick dude")
        elif vibe < 20:
            await ctx.send("Vibin hard")
        else:
            await ctx.send("So much :cum:")
