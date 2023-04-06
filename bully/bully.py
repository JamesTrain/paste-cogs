import discord
from redbot.core import commands
from .pcx_lib import type_message

pank = 295400354160443403

class bully(commands.Cog):
    #This Cog takes the previous message and turns it into CaMeL cAsInG

    @commands.command(aliases=["b"])
    async def sarcasm(self, ctx: commands.Context):
        #Define the command for RedBot
        messageObject = (await ctx.channel.history(limit=2).flatten())[1]
        message = messageObject.content
        
        if not message:
            message = "I can't translate that!"
        if messageObject.author.id == pank:
            await type_message(
                ctx.channel,
                self.sarcog_string("Joey is a fucking idiot"),
                allowed_mentions=discord.AllowedMentions(
                    everyone=False, users=False, roles=False),
            )
            return;
        
        await type_message(
            ctx.channel,
            self.sarcog_string(message),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False),
        )
        
    @staticmethod
    def sarcog_string(x):
        #Sarcasm and return string
        output = []
        for let in range(len(x)):
            if let%2==0:
                output.append(x[let].lower())
            else:
                output.append(x[let].upper())
        return "".join(output)
