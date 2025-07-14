# Author - Shaolin Monk
 
from .china import chinese

async def setup(bot):
    await bot.add_cog(china())
