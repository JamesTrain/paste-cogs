import discord; import re
from discord.ext import commands
from redbot.core import commands
from .split import split_into_sentences

# example url
# https://lmgtfy.app/?q=fuck+this+nonsense%3F

#Redbot cog that takes the above message and converts it to a "lmgtfy" link.
class lmgtfy(commands.Cog):

    @commands.command(pass_context=True)
    async def lmgtfy(self, ctx: commands.Context):
        message = (await ctx.channel.history(limit=2).flatten())[1].content
 
        def google(io):
            sentence = split_into_sentences(io)
            for i in sentence:
                if '?' in i[::-1]:
                    o = re.split(r'\s|(?<!\d)[\?](?!\d)/gm', i)
                    output = "https://lmgtfy.app/?q="
                    for l in o:
                        output = ''.join([output, l+'+'])
                    output = output[:-1] + '?'

                    embed = discord.Embed(
                        title = 'LMGTFY',
                        description = 'You lazy POS. Google it yourself next time',
                        colour = discord.Colour.red()
                    )
                    embed.add_field(name="Here.", value=output)
                    return embed
                elif '?' not in i[::-1]:
                    continue
                else:
                    return "I can't seem to find a question."
            
        google(message)