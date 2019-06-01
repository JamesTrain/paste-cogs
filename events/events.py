import asyncio
import io
import aiohttp

from collections import namedtuple

import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

BaseCog = getattr(commands, "Cog", object)

class Events(BaseCog):
    """Paste Points cog settings"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374574)
        default_guild = {}
        self.config.register_guild(**default_guild)

    @commands.group(autohelp=False)
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    async def events(self, ctx):
        """These Are Events"""

        await ctx.send("Yeye")