from .jail import Jail


async def setup(bot):
    await bot.add_cog(Jail(bot))

# Author - Daniel Bush, A.K.A. Daddy 