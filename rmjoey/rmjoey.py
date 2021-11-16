import discord
from redbot.core import commands

class rmjoey(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 194299256750735361:
            await message.delete()
            await message.channel.send(f"You can't do that, {message.author.mention}")
