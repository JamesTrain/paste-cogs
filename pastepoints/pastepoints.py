import asyncio
from datetime import datetime

import discord
from redbot.core import Config, checks, commands

# Paste Points are the new Bitcoin
class PastePoints(commands.Cog):
    """My custom cog"""

    @commands.group(autohelp=False)
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def points(self, ctx, message):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("This works")
        await message.add_reaction(emoji="redCross:423541694600970243")