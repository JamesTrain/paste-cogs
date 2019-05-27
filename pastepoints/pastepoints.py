import asyncio
import io
import aiohttp
import logging

from collections import namedtuple
from datetime import datetime

import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

# Paste Points are the new Bitcoin

BaseCog = getattr(commands, "Cog", object)

class PastePoints(BaseCog):
    """Paste Points cog settings"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374573)
        default_guild = {}
        self.config.register_guild(**default_guild)
        self.config.register_user(karma=0)

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
            upemoji = self.bot.get_emoji(397064398830829569)
            downemoji = self.bot.get_emoji(272737368916754432)
            await message.add_reaction(upemoji)
            await message.add_reaction(downemoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being added, and updates karma.
        Ignores Private Channels and users reacting to their own message.
        """
        await self._check_reaction(reaction, user, added=True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being removed, and updates karma.
        Ignores Private Channels and users reacting to their own message.
        """
        await self._check_reaction(reaction, user, added=False)

    async def _check_reaction(self, reaction: discord.Reaction, user: discord.User, *, added: bool):
        message = reaction.message
        (author, channel, guild) = (message.author, message.channel, message.guild)
        if author == user or isinstance(channel, discord.abc.PrivateChannel):
            return
        emoji = reaction.emoji
        upvote = await self._is_upvote(guild, emoji)
        if upvote is not None:
            await self._add_karma(author, 1 if upvote == added else -1)

    async def _add_karma(self, user: discord.User, amount: int):
        settings = self.config.user(user)
        karma = await settings.karma()
        await settings.karma.set(karma + amount)