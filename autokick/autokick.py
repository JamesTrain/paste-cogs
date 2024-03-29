import asyncio, io, time

import aiohttp
import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

BaseCog = getattr(commands, "Cog", object)

class AutoKick(BaseCog):
    """Bye bye"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374573)
        default_guild = {}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            if (after.channel.id == 845055977182330901):
                time.sleep(1)
                await member.move_to(channel=None, reason="Get rekd nerd")
