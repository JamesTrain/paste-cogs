import discord
from redbot.core import commands

class rmjoey(commands.Cog):
    """
    Fuck Joey. No one likes Joey.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 249575158719840266:
            await message.delete()
