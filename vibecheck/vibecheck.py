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
    async def vibestats(self, ctx: commands.Context, user: discord.Member = None):
        """View vibe check statistics.
        
        Parameters
        ----------
        user : discord.Member, optional
            The user to check stats for. If not provided, shows your own stats.
        """
        try:
            target_user = user or ctx.message.author
            async with self.config.user(target_user).all() as user_data:
                if not user_data or 'vibe_scores' not in user_data or not user_data['vibe_scores']:
                    await ctx.send(f"{target_user.name} hasn't checked their vibes yet!")
                    return

                vibe_scores = user_data['vibe_scores']
                total_checks = len(vibe_scores)
                total_vibe = sum(vibe_scores)
                average = total_vibe / total_checks
                current_vibe = user_data.get('vibe', 0)

                stats_message = (
                    f"📊 **Vibe Statistics for {target_user.name}**\n"
                    f"Current Vibe: {current_vibe}\n"
                    f"Total Checks: {total_checks}\n"
                    f"Average Vibe: {average:.1f}\n"
                    f"Total Vibe Power: {total_vibe}\n"
                )
                await ctx.send(stats_message)
            
        except Exception as e:
            await ctx.send("An error occurred while fetching stats. Please try again later.")
            print(f"Error in vibestats: {e}")

    @commands.command()
    async def vibeboard(self, ctx: commands.Context, sort_by: str = "total"):
        """Show the vibe leaderboard for all users.
        
        Parameters
        ----------
        sort_by : str, optional
            How to sort the leaderboard. Can be 'total' or 'avg' (default: total)
        """
        try:
            # Get all users in the guild
            all_users = ctx.guild.members
            user_stats = []

            # Collect stats for all users
            for user in all_users:
                user_data = await self.config.user(user).all()
                if user_data and 'vibe_scores' in user_data and user_data['vibe_scores']:
                    vibe_scores = user_data['vibe_scores']
                    user_stats.append({
                        'name': user.name,
                        'total_vibe': sum(vibe_scores),
                        'average': sum(vibe_scores) / len(vibe_scores),
                        'checks': len(vibe_scores),
                        'avatar_url': user.display_avatar.url
                    })

            if not user_stats:
                await ctx.send("No vibe checks recorded yet!")
                return

            # Sort based on user preference
            sort_by = sort_by.lower()
            if sort_by == "avg":
                # Filter users with fewer than 150 checks for average leaderboard
                user_stats = [stats for stats in user_stats if stats['checks'] >= 150]
                
                if not user_stats: # Check if any users remain after filtering
                    await ctx.send("No users with at least 150 vibe checks found for the average leaderboard.")
                    return

                user_stats.sort(key=lambda x: x['average'], reverse=True)
                title = "🏆 Average Vibe Leaderboard"
            else:
                user_stats.sort(key=lambda x: x['total_vibe'], reverse=True)
                title = "🏆 Total Vibe Leaderboard"

            # Create embed
            embed = discord.Embed(
                title=title,
                color=discord.Color.gold()
            )

            # Create the header
            description = "```\n"
            description += f"{title}\n"
            description += "Rank  Name               Total  Checks  Avg\n"
            description += "────────────────────────────────────────────\n"

            # Format each entry
            for i, stats in enumerate(user_stats[:10], 1):
                rank = f"#{i}"
                name = stats['name'][:15]  # Truncate name if too long
                total = f"{stats['total_vibe']:,}"
                checks = str(stats['checks'])
                avg = f"{stats['average']:.1f}"

                # Format each field with proper spacing
                rank = f"{rank:<3}"
                name = f"{name:<15}"
                total = f"{total:>6}"
                checks = f"{checks:>6}"
                avg = f"{avg:>5}"

                description += f"{rank}  {name} {total} {checks} {avg}\n"

            description += "```"
            embed.description = description

            # Add footer with command hint
            embed.set_footer(text=f"Try [p]vibeboard {'total' if sort_by == 'avg' else 'avg'} to sort by {'total vibe power' if sort_by == 'avg' else 'average score'}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("An error occurred while fetching the leaderboard. Please try again later.")
            print(f"Error in vibeboard: {e}")

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def vibescan(self, ctx: commands.Context, channel: discord.TextChannel = None):
    #     """Scan channel(s) for past vibe checks and update user stats.
        
    #     Parameters
    #     ----------
    #     channel : discord.TextChannel, optional
    #         The specific channel to scan. If not provided, scans all channels.
    #     """
    #     try:
    #         progress_msg = await ctx.send("Starting vibe scan...")
            
    #         # Regular expression to match vibe check messages
    #         vibe_pattern = re.compile(r"<@!?(\d+)> checked their vibe and got \*\*(\d+)\*\*")
            
    #         total_messages = 0
    #         vibe_checks_found = 0
            
    #         # Use a dictionary to batch process user updates
    #         user_updates = {}  # {user_id: {scores: list(), name: str}}
            
    #         # Determine which channels to scan
    #         channels_to_scan = [channel] if channel else ctx.guild.text_channels
            
    #         # First pass: Collect all vibe data
    #         for channel in channels_to_scan:
    #             try:
    #                 await progress_msg.edit(content=f"Scanning {channel.mention}...")
                    
    #                 # Process messages in chunks for better performance
    #                 async for message in channel.history(limit=None, oldest_first=True):  # Process in chronological order
    #                     total_messages += 1
    #                     if total_messages % 5000 == 0:  # Update less frequently
    #                         await progress_msg.edit(content=f"Scanning {channel.mention}...\nProcessed {total_messages:,} messages")
                        
    #                     match = vibe_pattern.search(message.content)
    #                     if match:
    #                         vibe_checks_found += 1
    #                         user_id = int(match.group(1))
    #                         vibe_score = int(match.group(2))
                            
    #                         # Batch user updates
    #                         if user_id not in user_updates:
    #                             user = self.bot.get_user(user_id)
    #                             if user:
    #                                 user_updates[user_id] = {
    #                                     'scores': [],  # Use list to keep all scores
    #                                     'name': user.name
    #                                 }
                            
    #                         if user_id in user_updates:
    #                             user_updates[user_id]['scores'].append(vibe_score)
                            
    #             except discord.Forbidden:
    #                 await progress_msg.edit(content=f"⚠️ Cannot access {channel.mention}, skipping...")
    #                 continue
            
    #         if not user_updates:
    #             await progress_msg.edit(content="No vibe checks found!")
    #             return
                
    #         # Second pass: Bulk update users
    #         await progress_msg.edit(content="Processing updates...")
    #         processed_users = 0
    #         total_users = len(user_updates)
            
    #         for user_id, data in user_updates.items():
    #             user = self.bot.get_user(user_id)
    #             if user:
    #                 processed_users += 1
    #                 if processed_users % 10 == 0:  # Update progress every 10 users
    #                     await progress_msg.edit(content=f"Updating users... {processed_users}/{total_users}")
                    
    #                 # Get existing scores first
    #                 async with self.config.user(user).all() as user_data:
    #                     if 'vibe_scores' not in user_data:
    #                         user_data['vibe_scores'] = []
                        
    #                     # Add all scores in chronological order
    #                     user_data['vibe_scores'].extend(data['scores'])
    #                     # Update current vibe to the most recent one
    #                     if data['scores']:  # Only update if we found scores
    #                         user_data['vibe'] = data['scores'][-1]
            
    #         # Generate summary
    #         channel_scope = channel.mention if channel else "all channels"
    #         summary = (
    #             f"Scan complete for {channel_scope}!\n"
    #             f"Total messages scanned: {total_messages:,}\n"
    #             f"Vibe checks found: {vibe_checks_found:,}\n"
    #             f"Users updated: {len(user_updates)}\n\n"
    #             "Updates per user:\n"
    #         )
            
    #         for user_id, data in user_updates.items():
    #             new_vibes = len(data['scores'])
    #             if new_vibes > 0:
    #                 summary += f"- {data['name']}: {new_vibes:,} vibe(s)\n"
            
    #         await progress_msg.edit(content=summary)
            
    #     except Exception as e:
    #         await ctx.send(f"An error occurred while scanning for vibe checks: {e}")
    #         print(f"Error in vibescan: {e}")
