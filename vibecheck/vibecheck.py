import asyncio, io, re, datetime, time, os
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

print("Should be UTC{}".format(datetime.datetime.now()))

# Set timezone
os.environ['TZ'] = 'UTC'
time.tzset()

print("Should be EST{}".format(datetime.datetime.now()))

BaseCog = getattr(commands, "Cog", object)

class Vibecheck(BaseCog):
    """Check them vibes"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier = 974374574)
        default_guild = {}
        self.config.register_guild(**default_guild)
        self.config.register_user(vibe = 0)

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.config.register_user(lastran = datetime.datetime.strftime(yesterday, "%Y-%m-%d"))

    @commands.command()
    async def vibecheck(self, ctx: commands.Context):
        """Check your vibes"""
        lastranstr = await self.config.user(ctx.message.author).lastran()
        lastran = datetime.datetime.strptime(lastranstr, "%Y-%m-%d").date()

        if datetime.datetime.now() == lastran:
            vibe = await self.config.user(ctx.message.author).vibe()
            await ctx.send("You rolled a **{}** today.".format(vibe))
        else:
            await self.config.user(ctx.message.author).lastran.set(
                datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
            )

            vibe = randint(1, 20)
            await self.config.user(ctx.message.author).vibe.set(vibe)

            if vibe == 1:
                comment = "lmaooo"
            elif vibe < 6:
                comment = "Sucks for you bro"
            elif vibe < 11:
                comment = "I guess that's fine"
            elif vibe < 16:
                comment = "Pretty sick dude"
            elif vibe < 20:
                comment = "Vibin hard"
            else:
                comment = "Okay King"

            await ctx.send(":game_die: {} checked their vibe and got **{}**\n{}".format(
                ctx.message.author.mention,vibe,comment)
            )