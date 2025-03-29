import datetime
import time
import os
from typing import Dict, Optional

import discord
from redbot.core import Config, commands

# Set timezone
os.environ['TZ'] = 'EST'
time.tzset()

class Vibecheck(commands.Cog):
    """Check them vibes
    
    A cog that allows users to check their daily vibes.
    Users can check their vibes once per day, getting a random score
    between 0 and 20 with corresponding comments.
    """

    VIBE_COMMENTS: Dict[int, str] = {
        0: "Literally die idiot 💀",
        1: "Uh oh stinky!",
        2: "Your vibes are catastrophically bad",
        4: "That's gonna be an oof from me dog",
        6: "Not looking good fam",
        8: "You might want to go back to bed",
        10: "That's almost a vibe",
        12: "Getting better, keep it up",
        14: "Alright, now that's a meme",
        16: "It's gonna be a good day :)",
        18: "Absolutely vibing!",
        20: "IMMACULATE VIBES, YOUR MAJESTY 👑"
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374574)
        default_guild = {}
        self.config.register_guild(**default_guild)
        self.config.register_user(vibe=0)

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.config.register_user(lastran=datetime.datetime.strftime(yesterday, "%Y-%m-%d"))

    def _get_vibe_comment(self, vibe: int) -> str:
        """Get the appropriate comment for a given vibe score."""
        for threshold in sorted(self.VIBE_COMMENTS.keys(), reverse=True):
            if vibe >= threshold:
                return self.VIBE_COMMENTS[threshold]
        return self.VIBE_COMMENTS[0]

    @commands.command()
    async def vibecheck(self, ctx: commands.Context):
        """Check your vibes for the day.
        
        Users can only check their vibes once per day.
        Returns a random score between 0 and 20 with a corresponding comment.
        """
        try:
            lastranstr = await self.config.user(ctx.message.author).lastran()
            lastran = datetime.datetime.strptime(lastranstr, "%Y-%m-%d").date()

            if datetime.date.today() == lastran:
                vibe = await self.config.user(ctx.message.author).vibe()
                await ctx.send("You rolled a **{}** today.".format(vibe))
            else:
                await self.config.user(ctx.message.author).lastran.set(
                    datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
                )
                    
                vibe = time.time_ns() % 21  # Generate random number between 0 and 20
                await self.config.user(ctx.message.author).vibe.set(vibe)

                comment = self._get_vibe_comment(vibe)
                await ctx.send(":game_die: {} checked their vibe and got **{}**\n{}".format(
                    ctx.message.author.mention, vibe, comment
                ))
        except Exception as e:
            await ctx.send("An error occurred while checking your vibes. Please try again later.")
            print(f"Error in vibecheck: {e}")
