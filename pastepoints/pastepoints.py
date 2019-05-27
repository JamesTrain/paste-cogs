import asyncio
from datetime import datetime

import discord
from redbot.core import Config, checks, commands

# Paste Points are the new Bitcoin

BaseCog = getattr(commands, "Cog", object)

class PastePoints(BaseCog):
    """Paste Points cog settings"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374573)

    @commands.group(autohelp=False)
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    async def points(self, ctx):
        """Paste Points Are Cool"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    @points.command(name="test")
    async def _points_test(self, ctx):
        """This is a huge meme"""
        await ctx.send("This is the biggest meme")
        await ctx.send("This is the biggest meme x2")

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author.id == self.bot.user.id):
            return
        if (message.channel.id == 331655111644545027):
            await message.add_reaction('\u2705')
            await message.add_reaction('\u274C')
        upemoji = '<:bolbmoji:397064398830829569>'
        downemoji = '<:FeelsBadMan:272737368916754432>'
        await message.add_reaction(upemoji)
        await message.add_reaction(downemoji)
