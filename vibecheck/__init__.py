from .vibecheck import Vibecheck

async def setup(bot):
    await bot.add_cog(Vibecheck(bot))