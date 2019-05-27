import asyncio
from datetime import datetime

import discord
from redbot.core import Config, checks, commands

# Paste Points are the new Bitcoin
class PastePoints(commands.Cog):
    """Paste Points cog settings"""

    @commands.group(autohelp=False)
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    async def points(self, ctx):
        await ctx.send("This works")

    async def on_message(self, ctx):
        await ctx.send("memes")