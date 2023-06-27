from .pasteon import Pasteon

async def setup(bot):
    await bot.add_cog(Pasteon(bot))