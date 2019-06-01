import asyncio
import contextlib
from datetime import datetime as dt, timedelta

import discord
from redbot.core import commands
from redbot.core import Config, commands, checks
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import pagify, warning

from .helpers import (
    parse_time,
    allowed_to_create,
    get_event_embed,
    allowed_to_edit,
    check_event_start,
)

from .menus import event_menu

BaseCog = getattr(commands, "Cog", object)

class Events(BaseCog):
    """Event Manager Help Message"""

    
    
    def __init__(self, bot):
        self.bot = bot
        self.settings  = Config.get_conf(self, identifier=974374574)
        default_guild = {"events": [], "next_available_id": 1}
        self.settings.register_guild(**default_guild)


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


    @events.command(name="list")
    async def _events_list(self, ctx):
        """Lists Events"""
        await ctx.send("This is the list meme")


    @events.command(name="add")
    async def _events_add(self, ctx: commands.Context):
        """
        Wizard-style event creation tool.
        The event will only be created if all information is provided properly.
        If a minimum required role has been set, users must have that role or
        higher, be in the mod/admin role, or be the guild owner in order to use this command
        """
        author = ctx.author
        guild = ctx.guild

        event_id = await self.settings.guild(guild).next_available_id()

        creation_time = ctx.message.created_at.timestamp()
        print ("DEBUG: Creation_time: ", creation_time)
        await ctx.send("Enter a name for the event: ")

        def same_author_check(msg):
            return msg.author == author

        msg = await self.bot.wait_for("message", check=same_author_check)
        name = msg.content
        if len(name) > 256:
            await ctx.send(
                _("That name is too long! Event names " "must be 256 charcters or less.")
            )
            return
        await ctx.send(
            "Enter the amount of time from now the event will take "
            "place (valid units are w, d, h, m, s): "
        )
        msg = await self.bot.wait_for("message", check=same_author_check)
        start_time = parse_time(creation_time, msg)
        if start_time is None:
            await ctx.send("Something went wrong with parsing the time you entered!")
            return
        await ctx.send("Enter a description for the event: ")
        msg = await self.bot.wait_for("message", check=same_author_check, timeout=60)
        if len(msg.content) > 1000:
            await ctx.send("Your description is too long!")
            return
        else:
            desc = msg.content

        new_event = {
            "id": event_id,
            "creator": author.id,
            "create_time": creation_time,
            "event_name": name,
            "event_start_time": start_time,
            "description": desc,
            "has_started": False,
            "participants": [author.id],
        }
        async with self.settings.guild(guild).events() as event_list:
            event_list.append(new_event)
            event_list.sort(key=lambda x: x["create_time"])
            await ctx.send(embed=get_event_embed(guild, ctx.message.created_at, new_event))


    @events.command(name="remove")
    async def _events_remove(self, ctx):
        """Adds Events"""
        await ctx.send("This is the remove meme")

    @events.command(name="edit")
    async def _events_edit(self, ctx):
        """Adds Events"""
        await ctx.send("This is the edit meme")