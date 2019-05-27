import asyncio
from datetime import datetime

import discord
from discord.utils import get
from redbot.core import Config, checks, commands

# Paste Points are the new Bitcoin

class PastePoints(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def points(self, ctx, message):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("This works")
        await message.add_reaction(message, emoji="redCross:423541694600970243")
    
    async def on_message(self, message):
        await message.add_reaction(message, emoji="redCross:423541694600970243")