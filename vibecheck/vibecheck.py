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

    @commands.command()
    async def vibecheck(self, ctx: commands.Context):
        """Check your vibes"""
        await ctx.send(":game_die: {} checked their vibe and got {}".format(ctx.message.author.mention,randint(1, 20)))
