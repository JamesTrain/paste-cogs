from .pastepoints import PastePoints

def setup(bot):
    bot.add_cog(PastePoints(bot))