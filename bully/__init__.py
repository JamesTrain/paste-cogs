from .bully import bully


async def setup(bot):
    await bot.add_cog(bully())

# Author - Daniel Bush, A.K.A. Daddy