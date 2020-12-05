import asyncio
import io
import re
from collections import namedtuple
from datetime import date, datetime, timedelta
import mysql.connector

import aiohttp
import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

# I promise I'm not a fed

BaseCog = getattr(commands, "Cog", object)

upemoji_id = 397064398830829569
downemoji_id = 272737368916754432
meme_channel_id = 331655111644545027

class MessageLog(BaseCog):
    """Message Log cog settings meme"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374515)
        default_guild = {}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self._insert_message(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being added, and updates karma."""
        await self._check_reaction(reaction, user, added=True, Reaction.message)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User, message):
        """Fires when the bot sees a reaction being removed, and updates karma."""
        await self._check_reaction(reaction, user, added=False, message)

    async def _check_reaction(self, reaction: discord.Reaction, user: discord.User, *, added: bool, message):
        message = reaction.message
        (author, channel, guild) = (message.author, message.channel, message.guild)
        if author == user:
            return
        if (reaction.emoji.id == upemoji_id):
            await self._add_karma(author, 1 if added == True else -1, message)
        elif (reaction.emoji.id == downemoji_id):
            await self._add_karma(author, -1 if added == True else 1, message)

    async def _add_karma(self, user: discord.User, amount: int):
        cnx = mysql.connector.connect(
        host="localhost",
        user="pastebot",
        password="8Kv7@D5S@HuQ",
        database="paste"
        )
        cursor = cnx.cursor()

        # Get current upvotes
        cursor.execute("SELECT upvotes FROM messages WHERE message_id = '{}'".format(message.id))
        upvotes = mycursor.fetchall()

        #Add 1 to the count
        upvotes += amount
        cursor.execute("SELECT upvotes FROM messages WHERE message_id = '{}'".format(message.id))

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()

    async def _insert_message(self, message):
        cnx = mysql.connector.connect(
        host="localhost",
        user="pastebot",
        password="8Kv7@D5S@HuQ",
        database="paste"
        )
        cursor = cnx.cursor()

        date = datetime.now()

        add_message = ("INSERT INTO messages "
                    "(creation_date, message_id, member_id, channel_id, upvotes, downvotes) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")

        data_message = (date, str(message.id), str(message.author.id), str(message.channel.id), '0', '0')

        # Insert new message
        cursor.execute(add_message, data_message)

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()