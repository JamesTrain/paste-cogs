import asyncio
from datetime import datetime

import discord
from redbot.core import Config, checks, commands

# Paste Points are the new Bitcoin

BaseCog = getattr(commands, "Cog", object)

class PastePoints(BaseCog):
    """Paste Points cog settings"""

    @commands.command()
    async def points(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
