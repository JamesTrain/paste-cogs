from .bully import bully


async def setup(bot):
    await bot.add_cog(bully(bot))

# Author - Daniel Bush, A.K.A. Daddy