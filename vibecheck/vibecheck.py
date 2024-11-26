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

# Set timezone
os.environ['TZ'] = 'EST'
time.tzset()

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
        print("Last ran {}. Now {}".format(lastran, datetime.date.today()))

        if datetime.date.today() == lastran:
            vibe = await self.config.user(ctx.message.author).vibe()
            await ctx.send("You rolled a **{}** today.".format(vibe))
        else:
            await self.config.user(ctx.message.author).lastran.set(
                datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
            )

            if ctx.message.author.id == 194299256750735361:
                vibe = 20
            elif ctx.message.author.id == 295400354160443403:
                vibe = 1
            else:
                vibe = randint(0, 20)
                
            await self.config.user(ctx.message.author).vibe.set(vibe)

            if vibe < 1:
                comment = "Literally die idiot 💀"
            elif vibe < 2:
                comment = "Uh oh stinky!"
            elif vibe < 6:
                comment = "That's gonna be an oof from me dog"
            elif vibe < 11:
                comment = "That's almost a vibe"
            elif vibe < 16:
                comment = "Alright, now that's a meme"
            elif vibe < 20:
                comment = "It's gonna be a good day :)"
            else:
                comment = "Okay King"

            await ctx.send(":game_die: {} checked their vibe and got **{}**\n{}".format(
                ctx.message.author.mention,vibe,comment)
            )
