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
        embed = discord.Embed(title="Event Planner", description="How to use the event planner", color=0x09616D)
        embed.add_field(name="[p]events list", value="Show a list of upcoming events.", inline=False)
        embed.add_field(name="[p]events add", value="Add a new event.", inline=False)
        embed.add_field(name="[p]events remove", value="Delete an event.", inline=False)
        embed.add_field(name="[p]events edit", value="Change an event.", inline=False)
        await ctx.send(embed=embed)

    @events.command(name="add")
    async def _events_list(self, ctx):
        """Lists Events"""
        await ctx.send("This is the biggest meme")
        await ctx.send("This is the biggest meme x2")