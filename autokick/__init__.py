from .autokick import AutoKick

def setup(bot):
    bot.add_cog(AutoKick(bot))