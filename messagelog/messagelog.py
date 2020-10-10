import asyncio
import io
import re
from collections import namedtuple

import aiohttp
import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

# I promise I'm not a fed

BaseCog = getattr(commands, "Cog", object)

class MessageLog(BaseCog):
    """Message Log cog settings meme"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374515)
        default_guild = {}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being added, and updates karma."""
        print("DEBUG :: Reaction Added")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being removed, and updates karma."""
        print("DEBUG :: Reaction Removed")