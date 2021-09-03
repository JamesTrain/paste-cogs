import discord
from redbot.core import commands
from .pcx_lib import type_message

class lmgtfy(commands.Cog):
    @commands.command(aliases=[""])
    async def lmgtfy(self, ctx:commands.Context):
        message = (await ctx.channel.history(limit=2).flatten())[1].content
        if not message:
            message = "This isn't a question. You a dumb person."
        else:
            await type_message(
                ctx.channel,
                self.lmgtfy(ctx, User_Mention),
                allowed_mentions=discord.AllowedMentions(
                    everyone=False, users=False,
                    roles=False
                ),
            )

    def lmgtfy (self, ctx, User_Mention):
        return "This cog loaded properly"