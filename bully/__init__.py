from .bully import Bully


async def setup(bot):
    await bot.add_cog(Bully(bot))

# Author - Daniel Bush, A.K.A. Daddy