import asyncio
import io
import aiohttp
import re

from collections import namedtuple

import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

# Don't join the furry channel

BaseCog = getattr(commands, "Cog", object)

class AutoKick(BaseCog):
    """Furry is bad"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374573)
        default_guild = {}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if (after.voice.voice_channel.id == 502108640530923520):
            a = self.bot.get_channel(364238602957226004)
            await a.send("FUCKKKKKKK")
            #await after.id.move_to(channel=None, reason="No Furries Allowed")