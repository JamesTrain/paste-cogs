import datetime
import time
import os
import re
from typing import Dict, Optional, List

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red

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
        18: "LET'S GOOOOOO",
        20: "IMMACULATE VIBES, YOUR MAJESTY 👑"
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374574)
        default_guild = {}
        self.config.register_guild(**default_guild)
        
        # Store both current vibe and vibe history
        self.config.register_user(
            vibe=0,
            vibe_scores=[],  # List to store all vibe scores
            lastran=datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1), "%Y-%m-%d")
        )

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
                
                # Update both current vibe and vibe history
                await self.config.user(ctx.message.author).vibe.set(vibe)
                async with self.config.user(ctx.message.author).all() as user_data:
                    if 'vibe_scores' not in user_data:
                        user_data['vibe_scores'] = []
                    user_data['vibe_scores'].append(vibe)

                comment = self._get_vibe_comment(vibe)
                await ctx.send(":game_die: {} checked their vibe and got **{}**\n{}".format(
                    ctx.message.author.mention, vibe, comment
                ))
        except Exception as e:
            await ctx.send("An error occurred while checking your vibes. Please try again later.")
            print(f"Error in vibecheck: {e}")

    @commands.command()
    async def vibestats(self, ctx: commands.Context):
        """View your vibe check statistics.
        
        Shows your current vibe, total checks, average vibe, and total vibe power.
        """
        try:
            async with self.config.user(ctx.message.author).all() as user_data:
                if not user_data or 'vibe_scores' not in user_data or not user_data['vibe_scores']:
                    await ctx.send("You haven't checked your vibes yet!")
                    return

                vibe_scores = user_data['vibe_scores']
                total_checks = len(vibe_scores)
                total_vibe = sum(vibe_scores)
                average = total_vibe / total_checks
                current_vibe = user_data.get('vibe', 0)

                stats_message = (
                    f"📊 **Vibe Statistics for {ctx.message.author.name}**\n"
                    f"Current Vibe: {current_vibe}\n"
                    f"Total Checks: {total_checks}\n"
                    f"Average Vibe: {average:.1f}\n"
                    f"Total Vibe Power: {total_vibe}\n"
                )
                await ctx.send(stats_message)
            
        except Exception as e:
            await ctx.send("An error occurred while fetching your stats. Please try again later.")
            print(f"Error in vibestats: {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def vibescan(self, ctx: commands.Context):
        """Scan all channels for past vibe checks and update user stats.
        
        This command requires administrator permissions.
        """
        try:
            progress_msg = await ctx.send("Starting vibe scan...")
            
            # Regular expression to match vibe check messages
            vibe_pattern = re.compile(r"<@!?(\d+)> checked their vibe and got \*\*(\d+)\*\*")
            
            total_messages = 0
            vibe_checks_found = 0
            users_updated = {}
            
            # Scan all text channels in the server
            for channel in ctx.guild.text_channels:
                try:
                    await progress_msg.edit(content=f"Scanning {channel.mention}...")
                    async for message in channel.history(limit=None):
                        total_messages += 1
                        if total_messages % 1000 == 0:
                            await progress_msg.edit(content=f"Scanning {channel.mention}...\nProcessed {total_messages} messages")
                        
                        match = vibe_pattern.search(message.content)
                        if match:
                            vibe_checks_found += 1
                            user_id = int(match.group(1))
                            vibe_score = int(match.group(2))
                            
                            # Get the user object
                            user = self.bot.get_user(user_id)
                            if user:
                                if user_id not in users_updated:
                                    users_updated[user_id] = {"name": user.name, "count": 0}
                                
                                # Update user's vibe history
                                async with self.config.user(user).all() as user_data:
                                    if 'vibe_scores' not in user_data:
                                        user_data['vibe_scores'] = []
                                    if vibe_score not in user_data['vibe_scores']:
                                        user_data['vibe_scores'].append(vibe_score)
                                        users_updated[user_id]["count"] += 1
                except discord.Forbidden:
                    continue  # Skip channels we can't read
            
            # Generate summary
            summary = (
                f"Scan complete!\n"
                f"Total messages scanned: {total_messages:,}\n"
                f"Vibe checks found: {vibe_checks_found:,}\n"
                f"Users updated: {len(users_updated)}\n\n"
                "Updates per user:\n"
            )
            
            for user_id, data in users_updated.items():
                if data["count"] > 0:
                    summary += f"- {data['name']}: {data['count']} new vibe(s)\n"
            
            await progress_msg.edit(content=summary)
            
        except Exception as e:
            await ctx.send(f"An error occurred while scanning for vibe checks: {e}")
            print(f"Error in vibescan: {e}")
