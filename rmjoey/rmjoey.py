import discord
from redbot.core import commands

class rmjoey(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 295400354160443403:
            await message.delete()
            await message.channel.send(f"You can't do that, {message.author.mention}")

