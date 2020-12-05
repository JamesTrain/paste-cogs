import asyncio
import io
import re
from collections import namedtuple

import aiohttp
import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import box, pagify

# Paste Points are the new Bitcoin

BaseCog = getattr(commands, "Cog", object)

upemoji_id = 397064398830829569
downemoji_id = 784724908189548554
channel_id = 331655111644545027

class PastePoints(BaseCog):
    """Paste Points cog settings meme"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374573)
        default_guild = {}
        self.config.register_guild(**default_guild)
        self.config.register_user(karma=0)

    @commands.command()
    async def pp(self, ctx: commands.Context, top: int = 10):
        """Prints out the karma leaderboard.
        Defaults to top 10. Use negative numbers to reverse the leaderboard.
        """
        reverse = True
        if top == 0:
            top = 10
        elif top < 0:
            reverse = False
            top = -top
        members_sorted = sorted(
            await self._get_all_members(ctx.bot), key=lambda x: x.karma, reverse=reverse
        )
        if len(members_sorted) < top:
            top = len(members_sorted)
        topten = members_sorted[:top]
        highscore = ""
        place = 1
        for member in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += "{} | ".format(member.name).ljust(18 - len(str(member.karma)))
            highscore += str(member.karma) + "\n"
            place += 1
        if highscore != "":
            for page in pagify(highscore, shorten_by=12):
                await ctx.send(box(page, lang="py"))
        else:
            await ctx.send("No one has any karma 🙁")

    @commands.command()
    @checks.is_owner()
    async def setpp(self, ctx: commands.Context, user: discord.Member, amount: int):
        """Resets a user's karma."""
        await self.config.user(user).karma.set(amount)
        await ctx.send("{}'s karma has been set.".format(user.display_name))

    async def _get_all_members(self, bot):
        """Get a list of members which have karma.
        Returns a list of named tuples with values for `name`, `id`, `karma`.
        """
        member_info = namedtuple("Member", "id name karma")
        ret = []
        for member in bot.get_all_members():
            if any(member.id == m.id for m in ret):
                continue
            karma = await self.config.user(member).karma()
            if karma == 0:
                continue
            ret.append(member_info(
                id=member.id, name=str(member), karma=karma))
        return ret

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author.id == self.bot.user.id or (message.attachments == [] and message.embeds == [] and re.search(r"http:\/\/|https:\/\/", message.content) == None)):
            return
        if (message.channel.id == channel_id):
            upemoji = self.bot.get_emoji(upemoji_id)
            downemoji = self.bot.get_emoji(downemoji_id)
            await message.add_reaction(upemoji)
            await message.add_reaction(downemoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being added, and updates karma."""
        await self._check_reaction(reaction, user, added=True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        """Fires when the bot sees a reaction being removed, and updates karma."""
        await self._check_reaction(reaction, user, added=False)

    async def _check_reaction(self, reaction: discord.Reaction, user: discord.User, *, added: bool):
        message = reaction.message
        (author, channel, guild) = (message.author, message.channel, message.guild)
        if author == user:
            return
        if (reaction.emoji.id == upemoji_id):
            await self._add_karma(author, 1 if added == True else -1)
        elif (reaction.emoji.id == downemoji_id):
            await self._add_karma(author, -1 if added == True else 1)

    async def _add_karma(self, user: discord.User, amount: int):
        settings = self.config.user(user)
        karma = await settings.karma()
        await settings.karma.set(karma + amount)