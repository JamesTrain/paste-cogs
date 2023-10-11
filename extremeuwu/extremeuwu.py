import discord
from redbot.core import commands
from .pcx_lib import type_message

class extremeuwu(commands.Cog):
    #The newer crazier UwU command

    @commands.command(aliases=["xuwu"])
    async def extremeuwu(self, ctx: commands.Context):
        #Define the command for RedBot
        messages = [msg async for msg in ctx.channel.history(limit=2)]
        messageObject = messages[1]
        message = messageObject.content
        if not message:
            message = "***OMAE WA MOU SHINDEIRU***"
        else:
            await type_message(
            ctx.channel,
            self.exuwu(message),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False),
        )
        
    @staticmethod
    def exuwu(message_input):
        output = ''
        vowels = '[a,e,i,o,u,y]'
        for letter in message_input.lower():
            if letter not in vowels:
                output += letter
            elif letter in vowels:
                if letter == 'a':
                    output += 'AwA'
                elif letter == 'e':
                    output += 'EwE'
                elif letter == 'i':
                    output += 'IwI'
                elif letter == 'o':
                    output += 'OwO'
                elif letter == 'u':
                    output += 'UwU'
                elif letter == 'y':
                    output += 'YwY'
        return output
