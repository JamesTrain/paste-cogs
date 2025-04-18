"""
Mass voice channel move/transfer cog for Red Discord Bot
"""

from .massmove import Massmove

__red_end_user_data_statement__ = "This cog does not persistently store any data or metadata about users."

async def setup(bot):
    await bot.add_cog(Massmove(bot)) 