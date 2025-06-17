import datetime
import time
import os
import re
import asyncio
from typing import Dict, Optional, List, Union

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils import AsyncIter

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
        default_guild = {
            "vibe_king_role_id": 1362271069666410689,  # Store the VIBE KING role ID
            "breeder_role_id": 898070614403846155  # Store the breeder role ID
        }
        self.config.register_guild(**default_guild)
        
        # Store both current vibe and vibe history
        self.config.register_user(
            vibe=0,
            vibe_scores=[],  # List to store all vibe scores
            lastran=datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1), "%Y-%m-%d"),
            is_vibe_king=False  # Track if user currently has VIBE KING role
        )

        # Birthday message for special occasions
        self.BIRTHDAY_MESSAGE = "🎂 HAPPY BIRTHDAY! 🎉 On your special day, your vibes are IMMACULATE! 🎈"
        
        # Start the background task to check for midnight
        self.midnight_task = asyncio.create_task(self._schedule_midnight_reset())

    async def _schedule_midnight_reset(self):
        """Schedule the role reset to occur at midnight."""
        await self.bot.wait_until_ready()
        while self == self.bot.get_cog("Vibecheck"):
            now = datetime.datetime.now()
            # Calculate time until next midnight
            tomorrow = (now + datetime.timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            seconds_until_midnight = (tomorrow - now).total_seconds()
            
            # Sleep until midnight
            await asyncio.sleep(seconds_until_midnight)
            
            # Reset vibe king roles at midnight
            await self._reset_vibe_king_roles()
            
            # Sleep a bit to avoid double execution
            await asyncio.sleep(60)
            
    async def _reset_vibe_king_roles(self):
        """Reset all VIBE KING roles at midnight."""
        try:
            # Process all guilds the bot is in
            async for guild in AsyncIter(self.bot.guilds):
                vibe_king_role_id = await self.config.guild(guild).vibe_king_role_id()
                if not vibe_king_role_id:
                    continue
                    
                vibe_king_role = guild.get_role(vibe_king_role_id)
                if not vibe_king_role:
                    continue
                
                # Get all users with the VIBE KING role
                for member in guild.members:
                    if not member.bot and vibe_king_role in member.roles:
                        try:
                            # Remove the role
                            await member.remove_roles(vibe_king_role, reason="VIBE KING day has ended (midnight reset)")
                            # Update the user's config
                            await self.config.user(member).is_vibe_king.set(False)
                        except discord.Forbidden:
                            pass  # Bot doesn't have permission
                        except Exception as e:
                            print(f"Error removing VIBE KING role from {member.name}: {e}")
                            
            print(f"[Vibecheck] Reset VIBE KING roles at {datetime.datetime.now()}")
        except Exception as e:
            print(f"[Vibecheck] Error in reset_vibe_king_roles: {e}")

    def cog_unload(self):
        """Clean up when cog is unloaded."""
        if hasattr(self, 'midnight_task') and self.midnight_task:
            self.midnight_task.cancel()

    def _get_vibe_comment(self, vibe: int) -> str:
        """Get the appropriate comment for a given vibe score."""
        for threshold in sorted(self.VIBE_COMMENTS.keys(), reverse=True):
            if vibe >= threshold:
                return self.VIBE_COMMENTS[threshold]
        return self.VIBE_COMMENTS[0]

    def _is_fathers_day(self) -> bool:
        """Check if today is Father's Day (third Sunday in June)."""
        today = datetime.date.today()
        if today.month != 6:  # Father's Day is in June
            return False
        
        # Find the third Sunday in June
        first_day = datetime.date(today.year, 6, 1)
        days_until_first_sunday = (6 - first_day.weekday()) % 7  # 6 is Sunday
        first_sunday = first_day + datetime.timedelta(days=days_until_first_sunday)
        third_sunday = first_sunday + datetime.timedelta(weeks=2)
        
        return today == third_sunday

    async def _is_users_birthday(self, member: discord.Member) -> bool:
        """Check if today is the user's birthday using the Birthday cog."""
        # try:
        #     birthday_cog = self.bot.get_cog("birthday")
        #     if not birthday_cog:
        #         return False

        #     # Get the member's birthday data from the Birthday cog's config
        #     birthday_data = await birthday_cog.config.member(member).birthday()
        #     if not birthday_data:
        #         return False

        #     today = datetime.date.today()
        #     return today.month == birthday_data["month"] and today.day == birthday_data["day"]
        # except Exception as e:
        #     print(f"Error checking birthday: {e}")
        #     return False
        return False  # Temporarily disabled

    @commands.command()
    @commands.admin()
    async def vibetest(self, ctx: commands.Context, member: discord.Member = None):
        """Test command to inspect birthday cog data.
        
        This command helps debug the birthday cog integration by displaying
        available data about the birthday cog and user birthday settings.
        
        Parameters
        ----------
        member : discord.Member, optional
            The member whose birthday data to check. If not provided, checks your own.
        """
        try:
            target = member or ctx.author
            message = []
            
            # Get birthday cog
            birthday_cog = self.bot.get_cog("birthday")
            message.append(f"Birthday Cog Found: {birthday_cog is not None}")
            
            if birthday_cog:
                message.append(f"Birthday Cog Name: {birthday_cog.qualified_name}")
                message.append(f"Birthday Cog Version: {birthday_cog.__version__}")
                
                # Try to get birthday data
                try:
                    birthday_data = await birthday_cog.config.member(target).birthday()
                    message.append(f"\nBirthday Data for {target.name}:")
                    message.append(f"Raw Data: {birthday_data}")
                    if birthday_data:
                        message.append(f"Year: {birthday_data.get('year')}")
                        message.append(f"Month: {birthday_data.get('month')}")
                        message.append(f"Day: {birthday_data.get('day')}")
                except Exception as e:
                    message.append(f"\nError getting birthday data: {e}")
                
                # Check if guild is setup
                try:
                    is_setup = await birthday_cog.check_if_setup(ctx.guild)
                    message.append(f"\nGuild Setup Status: {is_setup}")
                except Exception as e:
                    message.append(f"\nError checking guild setup: {e}")
            
            await ctx.send("```\n" + "\n".join(message) + "\n```")
            
        except Exception as e:
            await ctx.send(f"An error occurred while testing birthday integration: {e}")
            print(f"Error in vibetest: {e}")

    @commands.command()
    async def vibecheck(self, ctx: commands.Context):
        """Check your vibes for the day.
        
        Users can only check their vibes once per day.
        Returns a random score between 0 and 20 with a corresponding comment.
        If you roll a 20, you get the VIBE KING role for the day!
        """
        try:
            lastranstr = await self.config.user(ctx.message.author).lastran()
            lastran = datetime.datetime.strptime(lastranstr, "%Y-%m-%d").date()

            if datetime.date.today() == lastran:
                vibe = await self.config.user(ctx.message.author).vibe()
                if await self.config.user(ctx.message.author).is_vibe_king():
                    await ctx.send("You already rolled today. Scroll up King :crown:")
                else:
                    await ctx.send("You already rolled today. Scroll up idiot :skull:")
            else:
                await self.config.user(ctx.message.author).lastran.set(
                    datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
                )
                    
                # Check if user ID is the special case that should always roll 0
                if str(ctx.message.author.id) == "899897827826745364":
                    vibe = 0
                # Check if it's the user's birthday
                elif await self._is_users_birthday(ctx.message.author):
                    vibe = 20
                    comment = self.BIRTHDAY_MESSAGE
                # Check if it's Father's Day and user has breeder role
                elif self._is_fathers_day():
                    breeder_role_id = await self.config.guild(ctx.guild).breeder_role_id()
                    if breeder_role_id and any(role.id == breeder_role_id for role in ctx.message.author.roles):
                        vibe = 20
                    else:
                        vibe = time.time_ns() % 21  # Generate random number between 0 and 20
                else:
                    vibe = time.time_ns() % 21  # Generate random number between 0 and 20
                
                # Update both current vibe and vibe history
                await self.config.user(ctx.message.author).vibe.set(vibe)
                async with self.config.user(ctx.message.author).all() as user_data:
                    if 'vibe_scores' not in user_data:
                        user_data['vibe_scores'] = []
                    user_data['vibe_scores'].append(vibe)

                # Get comment if not birthday (birthday comment is set above)
                if not await self._is_users_birthday(ctx.message.author):
                    comment = self._get_vibe_comment(vibe)
                
                message = ":game_die: {} checked their vibe and got **{}**\n{}".format(
                    ctx.message.author.mention, vibe, comment
                )
                
                # Add VIBE KING role if user rolled a 20
                if vibe == 20:
                    vibe_king_role_id = await self.config.guild(ctx.guild).vibe_king_role_id()
                    if vibe_king_role_id:
                        vibe_king_role = ctx.guild.get_role(vibe_king_role_id)
                    else:
                        vibe_king_role = discord.utils.get(ctx.guild.roles, name="VIBE KING")
                        
                        if not vibe_king_role and ctx.guild.me.guild_permissions.manage_roles:
                            try:
                                vibe_king_role = await ctx.guild.create_role(
                                    name="VIBE KING",
                                    color=discord.Color.gold(),
                                    reason="Created for vibecheck cog"
                                )
                                await self.config.guild(ctx.guild).vibe_king_role_id.set(vibe_king_role.id)
                            except discord.Forbidden:
                                vibe_king_role = None
                    
                    if vibe_king_role:
                        try:
                            await ctx.author.add_roles(vibe_king_role, reason="Rolled a 20 in vibecheck")
                            await self.config.user(ctx.message.author).is_vibe_king.set(True)
                            message += "\n👑 You've been granted the VIBE KING role for the day! 👑"
                        except discord.Forbidden:
                            pass  # Bot doesn't have permission, silently continue
                
                await ctx.send(message)
        except Exception as e:
            await ctx.send("An error occurred while checking your vibes. Please try again later.")
            print(f"Error in vibecheck: {e}")

    @commands.command()
    async def vibestats(self, ctx: commands.Context, user_or_limit: Optional[Union[discord.Member, int]] = None, limit_if_user_provided: Optional[int] = None):
        """View vibe check statistics.
        
        Parameters
        ----------
        user_or_limit : discord.Member or int, optional
            The user to check stats for, or the number of recent checks if no user is specified.
            If not provided, shows your own stats for all checks.
        limit_if_user_provided : int, optional
            The number of recent checks to show if a user was specified.
        """
        try:
            target_user: discord.Member
            num_checks: Optional[int] = None

            if user_or_limit is None and limit_if_user_provided is None:
                # [p]vibestats
                target_user = ctx.author
                num_checks = None
            elif isinstance(user_or_limit, discord.Member):
                # [p]vibestats @user
                # [p]vibestats @user 10
                target_user = user_or_limit
                num_checks = limit_if_user_provided
            elif isinstance(user_or_limit, int):
                # [p]vibestats 10
                target_user = ctx.author
                num_checks = user_or_limit
                if limit_if_user_provided is not None:
                    await ctx.send_help(ctx.command) 
                    return
            else: # Should not happen due to Union and Optional typing
                await ctx.send_help(ctx.command)
                return

            async with self.config.user(target_user).all() as user_data:
                if not user_data or 'vibe_scores' not in user_data or not user_data['vibe_scores']:
                    await ctx.send(f"{target_user.name} hasn't checked their vibes yet!")
                    return

                vibe_scores = user_data['vibe_scores']
                original_score_count = len(vibe_scores)

                if num_checks is not None and num_checks > 0:
                    if original_score_count < num_checks:
                        await ctx.send(f"{target_user.name} has only {original_score_count} vibe check(s), not {num_checks}.")
                        return
                    vibe_scores = vibe_scores[-num_checks:]
                
                if not vibe_scores: # Should only happen if num_checks was > 0 but original_score_count was 0 (caught above) or num_checks made it empty (also caught)
                    await ctx.send(f"{target_user.name} has no vibe checks for the specified criteria.")
                    return

                total_checks_considered = len(vibe_scores)
                total_vibe_considered = sum(vibe_scores)
                average_considered = total_vibe_considered / total_checks_considered if total_checks_considered > 0 else 0
                current_vibe = user_data.get('vibe', 0) # This is the last rolled vibe, independent of num_checks

                title_suffix = f" (Last {num_checks} Checks)" if num_checks else ""
                stats_message = (
                    f"📊 **Vibe Statistics for {target_user.name}{title_suffix}**\n"
                    f"Current Vibe (Last Roll): {current_vibe}\n"
                    f"Checks Considered: {total_checks_considered}\n"
                    f"Average Vibe (Considered): {average_considered:.1f}\n"
                    f"Total Vibe Power (Considered): {total_vibe_considered}\n"
                )
                await ctx.send(stats_message)
            
        except Exception as e:
            await ctx.send("An error occurred while fetching stats. Please try again later.")
            print(f"Error in vibestats: {e}")

    @commands.command()
    async def vibeboard(self, ctx: commands.Context, sort_by: str = "total", num_checks: Optional[int] = None):
        """Show the vibe leaderboard for all users.
        
        Parameters
        ----------
        sort_by : str, optional
            How to sort the leaderboard. Can be 'total', 'avg', or 'daily' (default: total).
        num_checks : int, optional
            Number of recent checks to consider if sorting by 'avg'. E.g., 'vibeboard avg 10'.
        """
        try:
            all_users = ctx.guild.members
            raw_user_data_list = []
            today_str = datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
            
            sort_by_lower = sort_by.lower()
            is_daily_board = sort_by_lower == "daily"
            
            daily_vibes_count = 0 # For daily board summary
            daily_vibes_total = 0 # For daily board summary

            for user_member in all_users:
                if user_member.bot:
                    continue
                user_config_data = await self.config.user(user_member).all()
                if user_config_data and 'vibe_scores' in user_config_data and user_config_data['vibe_scores']:
                    vibe_scores_list = user_config_data['vibe_scores']
                    
                    entry = {
                        'user_obj': user_member,
                        'all_scores': vibe_scores_list,
                        'current_vibe_today': None, # Populated if is_daily_board and rolled today
                        'rolled_today': False       # Populated if is_daily_board
                    }

                    if is_daily_board:
                        lastran = user_config_data.get('lastran', '')
                        if lastran == today_str:
                            entry['rolled_today'] = True
                            current_vibe_for_today = user_config_data.get('vibe', 0)
                            entry['current_vibe_today'] = current_vibe_for_today
                            # These are used for summary, not for sorting list directly here
                            daily_vibes_count += 1 
                            daily_vibes_total += current_vibe_for_today
                    
                    raw_user_data_list.append(entry)

            if not raw_user_data_list:
                await ctx.send("No vibe checks recorded yet in this server!")
                return

            user_stats_for_embed = []
            title = "🏆 Vibe Leaderboard" # Default title
            title_suffix = ""

            if is_daily_board:
                title = f"🏆 Today's Vibe Leaderboard ({today_str})"
                for raw_user in raw_user_data_list:
                    if raw_user['rolled_today']:
                        user_stats_for_embed.append({
                            'name': raw_user['user_obj'].name,
                            'total_vibe': raw_user['current_vibe_today'], # This is 'Vibe' for daily
                            'average': raw_user['current_vibe_today'],   # For data structure consistency
                            'checks': 1,                                 # For data structure consistency
                            'avatar_url': raw_user['user_obj'].display_avatar.url
                        })
                if not user_stats_for_embed:
                    await ctx.send(f"No vibe checks recorded for today ({today_str})!")
                    return
                user_stats_for_embed.sort(key=lambda x: x['total_vibe'], reverse=True)

            elif sort_by_lower == "avg":
                min_checks_for_default_avg = 150 # Existing behavior for "avg" without num_checks
                
                for raw_user in raw_user_data_list:
                    all_user_scores = raw_user['all_scores']
                    scores_to_consider = list(all_user_scores) # Make a copy
                    
                    num_actual_checks_for_avg = 0

                    if num_checks is not None and num_checks > 0: # User specified "avg N"
                        if len(scores_to_consider) < num_checks:
                            continue # Not enough checks for the specified limit
                        scores_to_consider = scores_to_consider[-num_checks:]
                        num_actual_checks_for_avg = len(scores_to_consider)
                        title_suffix = f" (Last {num_checks} Checks)"
                    else: # Default "avg" behavior (min 150 total checks, use all of them for avg)
                        if len(scores_to_consider) < min_checks_for_default_avg:
                            continue
                        # scores_to_consider remains all_user_scores
                        num_actual_checks_for_avg = len(scores_to_consider)
                        title_suffix = f" (Min {min_checks_for_default_avg} Total Checks)"
                    
                    if not scores_to_consider or num_actual_checks_for_avg == 0: 
                        continue

                    avg_vibe = sum(scores_to_consider) / num_actual_checks_for_avg
                    user_stats_for_embed.append({
                        'name': raw_user['user_obj'].name,
                        'total_vibe': sum(scores_to_consider), # Sum of the N scores considered
                        'average': avg_vibe,
                        'checks': num_actual_checks_for_avg, # Number of checks *considered*
                        'avatar_url': raw_user['user_obj'].display_avatar.url
                    })
                
                if not user_stats_for_embed:
                    msg_not_found = ""
                    if num_checks is not None and num_checks > 0:
                        msg_not_found = f"No users found with at least {num_checks} vibe checks for the average leaderboard."
                    else:
                        msg_not_found = f"No users with at least {min_checks_for_default_avg} total vibe checks found for the average leaderboard."
                    await ctx.send(msg_not_found)
                    return
                user_stats_for_embed.sort(key=lambda x: x['average'], reverse=True)
                title = f"🏆 Average Vibe Leaderboard{title_suffix}"

            else: # Default is "total" (sort_by_lower == "total" or invalid sort_by)
                  # num_checks parameter is ignored for "total" sort for now.
                title = "🏆 Total Vibe Leaderboard"
                for raw_user in raw_user_data_list:
                    all_scores = raw_user['all_scores'] 
                    if not all_scores: continue # Should have been caught by initial raw_user_data_list check
                    user_stats_for_embed.append({
                        'name': raw_user['user_obj'].name,
                        'total_vibe': sum(all_scores),
                        'average': sum(all_scores) / len(all_scores) if all_scores else 0,
                        'checks': len(all_scores),
                        'avatar_url': raw_user['user_obj'].display_avatar.url
                    })
                if not user_stats_for_embed: # Should be caught by raw_user_data_list check, but as safeguard
                    await ctx.send("No vibe checks recorded yet!")
                    return
                user_stats_for_embed.sort(key=lambda x: x['total_vibe'], reverse=True)
            
            # Create embed
            embed = discord.Embed(
                title=title, # Use the determined title
                color=discord.Color.gold()
            )

            description = "```\n"
            # description += f"{title}\n" # Title is now in embed.title

            if is_daily_board: # Specific summary for daily board
                if daily_vibes_count > 0:
                    daily_avg = daily_vibes_total / daily_vibes_count
                    description += f"Today's Average Vibe: {daily_avg:.1f}\n"
                    description += f"Today's Total Checks: {daily_vibes_count}\n\n"
                description += "Rank  Name                  Vibe\n"
                description += "───────────────────────────────\n"
            else: # Header for "total" and "avg" boards
                description += "Rank  Name               Total  Checks  Avg\n"
                description += "────────────────────────────────────────────\n"

            for i, stats in enumerate(user_stats_for_embed[:10], 1):
                rank_str = f"#{i}"
                name_str = stats['name'][:15] if not is_daily_board else stats['name'][:20]
                
                if is_daily_board:
                    vibe_str = str(stats['total_vibe']) # 'total_vibe' is today's vibe for daily
                    
                    rank_str = f"{rank_str:<3}"
                    name_str = f"{name_str:<20}"
                    vibe_str = f"{vibe_str:>5}"
                    
                    description += f"{rank_str}  {name_str} {vibe_str}\n"
                else: # "total" or "avg" board
                    total_str = f"{stats['total_vibe']:,}"
                    checks_str = str(stats['checks'])
                    avg_str = f"{stats['average']:.1f}"
                    
                    rank_str = f"{rank_str:<3}"
                    name_str = f"{name_str:<15}"
                    total_str = f"{total_str:>6}"
                    checks_str = f"{checks_str:>6}"
                    avg_str = f"{avg_str:>5}"
                    
                    description += f"{rank_str}  {name_str} {total_str} {checks_str} {avg_str}\n"

            description += "```"
            embed.description = description

            prefix = ctx.prefix
            footer_parts = []
            current_command_base = f"{prefix}vibeboard"

            if sort_by_lower != "total":
                footer_parts.append(f"{current_command_base} total")
            
            if sort_by_lower != "avg":
                footer_parts.append(f"{current_command_base} avg [N]")
            # If current is 'avg', suggest 'avg N' only if N wasn't specified. Otherwise, it's redundant.
            elif num_checks is None: # We are on 'avg' but not 'avg N'
                footer_parts.append(f"{current_command_base} avg N (e.g., {current_command_base} avg 10)")

            if sort_by_lower != "daily":
                footer_parts.append(f"{current_command_base} daily")
            
            if footer_parts:
                embed.set_footer(text="Also try: " + " or ".join(footer_parts))
            elif sort_by_lower == "avg" and num_checks is not None: # On "avg N", specific suggestion
                 embed.set_footer(text=f"Also try: {current_command_base} total or {current_command_base} daily or {current_command_base} avg (overall avg)")


            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred while fetching the leaderboard: {e}")
            print(f"Error in vibeboard: {e}")

    @commands.command()
    @commands.admin()
    async def vibereset(self, ctx: commands.Context, member: discord.Member = None):
        """Reset a user's daily vibe check.
        
        If no user is specified, resets your own vibe check.
        Only bot admins can use this command.
        
        Parameters
        ----------
        member : discord.Member, optional
            The member whose vibe check to reset. If not provided, resets your own.
        """
        try:
            target = member or ctx.author
            yesterday = datetime.datetime.strftime(
                datetime.date.today() - datetime.timedelta(days=1), 
                "%Y-%m-%d"
            )
            
            # Reset their lastran date to yesterday
            await self.config.user(target).lastran.set(yesterday)
            
            # If they had VIBE KING role, remove it
            if await self.config.user(target).is_vibe_king():
                vibe_king_role_id = await self.config.guild(ctx.guild).vibe_king_role_id()
                if vibe_king_role_id:
                    vibe_king_role = ctx.guild.get_role(vibe_king_role_id)
                    if vibe_king_role and vibe_king_role in target.roles:
                        try:
                            await target.remove_roles(vibe_king_role, reason="Vibe check reset by admin")
                        except discord.Forbidden:
                            pass  # Bot doesn't have permission
                await self.config.user(target).is_vibe_king.set(False)
            
            if target == ctx.author:
                await ctx.send("Your vibe check has been reset. You can now check your vibes again today!")
            else:
                await ctx.send(f"{target.mention}'s vibe check has been reset. They can now check their vibes again today!")
        except Exception as e:
            await ctx.send(f"An error occurred while resetting vibe check: {e}")
            print(f"Error in vibereset: {e}")

    # @commands.command()
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
