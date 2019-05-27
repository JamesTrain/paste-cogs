import asyncio
from datetime import datetime

import discord
from redbot.core import Config, checks, commands

# Paste Points are the new Bitcoin

BaseCog = getattr(commands, "Cog", object)

class PastePoints(BaseCog):
    """Paste Points cog settings"""

    @commands.guild_only()
    @checks.admin_or_permissions(administrator=True)
    async def points(self, ctx):
        await ctx.send("This works")
