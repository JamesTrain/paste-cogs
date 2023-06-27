from .rmjoey import rmjoey


async def setup(bot):
    await bot.add_cog(rmjoey(bot))

# Author - Daniel Bush, A.K.A. Daddy