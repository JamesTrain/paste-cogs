from .wordsub import WordSub
 
async def setup(bot):
    await bot.add_cog(WordSub(bot)) 