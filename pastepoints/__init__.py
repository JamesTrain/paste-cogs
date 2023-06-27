from .pastepoints import PastePoints

async def setup(bot):
    await bot.add_cog(PastePoints(bot))