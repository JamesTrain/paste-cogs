import discord
from redbot.core import commands
from .pcx_lib import type_message
from .insult_list import big_letters, final, final_list

class insult(commands.Cog):
    #Insult your friends
    @commands.command(aliases=["i"])
    async def insult(self, ctx: commands.Context, User_Mention):
        #Define the command for RedBot
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        if not message:
            message = "I big dumb dumb who can't think of insults"
        else:
            await type_message(
                ctx.channel,
                self.big_insults(ctx, User_Mention),
                allowed_mentions=discord.AllowedMentions(
                    everyone=False, users=False, roles=False),
            )
            
    def big_insults(self, ctx, User_Mention):
        # Pick and print insult from insult_list
        if '@' in User_Mention:
            return (f"**{User_Mention} IS A BIG**") + big_letters(final(final_list))
        else:
            return ("**Mention a User to insult them!**")
