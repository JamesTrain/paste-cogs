import discord
from redbot.core import commands
from .pcx_lib import type_message

class chinese(commands.Cog):
    #The latter half of black or chinese

    @commands.command(aliases=["china"])
    async def chinese(self, ctx: commands.Context):
        #Define the command for RedBot
        messages = [msg async for msg in ctx.channel.history(limit=2)]
        messageObject = messages[1]
        message = messageObject.content
        if not message:
            message = "sum ting wong"
        else:
            await type_message(
            ctx.channel,
            self.exuwu(message),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False),
        )
        
    @staticmethod
    def chinese(message_input):
        output = ''
        vowels = '[l, a , an ,d ]'
        for letter in message_input.lower():
            if letter not in vowels:
                output += letter
            elif letter in vowels:
                if letter == 'l':
                    output += 'r'
                elif letter == ' a ':
                    output += ' '
                elif letter == ' an ':
                    output += ' '
                elif letter == 'd ':
                    output += 't'
        return output
