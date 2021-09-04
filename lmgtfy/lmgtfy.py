#import necessary libs
import discord; import re
from redbot.core import commands
from .split import split_into_sentences

#version 0.1.0
class lmgtfy(commands.Cog):

    #init bot
    def __init__(self, bot):
        self.bot = bot

    #define command 'lmgtfy'
    @commands.command()
    async def lmgtfy(self, ctx: commands.Context):

        #grab message from discord
        message = (await ctx.channel.history(limit=2).flatten())[1].content

        #pipe message through 'split' function
        for i in split_into_sentences(message):

            #error/value handling to prevent repetition abuse
            if 'app/?' not in i:
                if 'q=' not in i[0:2]:
                    
                    #determine if question and return relevant results
                    if '?' in i[::-1]:
                        o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', i)
                        output = "https://lmgtfy.app/?q="
                        for l in o:
                            output = ''.join([output, l+'+'])
                        output = output[:-1]
                        await ctx.send(output)
                    elif '?' not in i[::-1]:
                        continue
                    else:
                        await ctx.send("I can't seem to find a question.")
