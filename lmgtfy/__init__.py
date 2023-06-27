from .lmgtfy import lmgtfy

async def setup(bot):
    await bot.add_cog(lmgtfy(bot))

# Author - Daniel Bush, A.K.A. Daddy