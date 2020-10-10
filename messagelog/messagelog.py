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

class MessageLog(BaseCog):
    """Message Log cog settings meme"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374515)
        default_guild = {}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        self._insert_message(message)

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