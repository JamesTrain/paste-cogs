import discord; import re
from redbot.core import commands
from .split import split_into_sentences

class lmgtfy(commands.Cog):
    """Redbot cog that takes a message and makes a 'lmgtfy' link out of it."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lmgtfy(self, ctx, Question):
        sentence = split_into_sentences(Question)
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