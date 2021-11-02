import discord
from redbot.core import commands

class rmjoey(commands.Cog):
    @bot.event
    async def on_message(message):
        if message.author.id == 295400354160443403 in message.content.lower():
            await message.delete()
            await message.channel.send(f"You can't do that, {message.author.mention}")
