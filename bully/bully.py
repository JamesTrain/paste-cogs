import discord
import datetime
from datetime import timezone
import random
import asyncio
from zoneinfo import ZoneInfo
from redbot.core import commands, Config

class Bully(commands.Cog):
    """A cog that bullies users by mocking their messages and assigns roles based on bully count."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374575)
        
        # Default configurations
        default_guild = {
            "class_clown_role_id": None,  # Role ID for Class Clown
            "stinky_loser_role_id": None,  # Role ID for Stinky Loser
            "random_bully_enabled": False, # Whether random bullying is enabled
        }
        default_user = {
            "bully_count": 0,  # Number of times bullied today
            "times_bullied_total": 0,
            "times_bullied_others": 0,
            "has_class_clown": False,  # Whether user currently has Class Clown role
            "has_stinky_loser": False  # Whether user currently has Stinky Loser role
        }
        
        self.config.register_guild(**default_guild)
        self.config.register_user(**default_user)
        
        # Funny messages for role assignments
        self.class_clown_messages = [
            "🤡 Congratulations {user}! You've been bullied so much, you're now officially our Class Clown! Maybe try being less of a target?",
            "🎪 Step right up, folks! {user} has been crowned our newest Class Clown! Three bullies in one day - that's talent!",
            "🎭 Breaking news: {user} has achieved peak clownery and earned the Class Clown role! Your parents must be so proud!",
            "🎪 Well well well, look who's joined the circus! {user} is our newest Class Clown! Keep up the great work at being a target!",
            "🤡 {user} has been bullied into the Class Clown role! At least you're entertaining us!"
        ]
        
        self.stinky_loser_messages = [
            "🦨 Phew! What's that smell? Oh, it's just {user} achieving their final form as a Stinky Loser!",
            "🗑️ Achievement unlocked: {user} has been bullied 5 times and is now officially a Stinky Loser! Impressive dedication to being a target!",
            "💩 Congratulations {user}! You've reached peak loser status and earned the coveted Stinky Loser role! Your mom would be so proud!",
            "🦨 Alert: {user} has transcended regular loserhood and achieved STINKY loser status! That's almost impressive!",
            "🗑️ Look everyone! {user} has been bullied so much they're now a certified Stinky Loser! At least you're good at something!"
        ]
        
        self.armed_for_random_bully = False
        self.next_bully_time = None
        self.manual_arm_event = asyncio.Event()

        # Start the midnight reset task
        self.midnight_task = asyncio.create_task(self._schedule_midnight_reset())
        self.random_bully_task = asyncio.create_task(self._random_bully_task())

    async def cog_check(self, ctx: commands.Context):
        """Prevents commands from being used in the disabled channel."""
        disabled_channel_id = 1282854167240773663
        return ctx.channel.id != disabled_channel_id

    @staticmethod
    def sarcog_string(x):
        """Sarcasm and return string"""
        output = []
        for let in range(len(x)):
            if let%2==0:
                output.append(x[let].lower())
            else:
                output.append(x[let].upper())
        return "".join(output)

    def cog_unload(self):
        """Clean up when cog is unloaded."""
        if hasattr(self, 'midnight_task') and self.midnight_task:
            self.midnight_task.cancel()
        if hasattr(self, 'random_bully_task') and self.random_bully_task:
            self.random_bully_task.cancel()

    async def _random_bully_task(self):
        """A background task that randomly bullies a user."""
        await self.bot.wait_until_ready()
        while self == self.bot.get_cog("Bully"):
            try:
                # Wait for a random interval between 1 and 2 hours
                wait_seconds = random.randint(3600, 7200)
                self.next_bully_time = datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=wait_seconds)
                
                # Wait for the sleep to finish OR for the event to be set
                sleep_task = asyncio.create_task(asyncio.sleep(wait_seconds))
                event_wait_task = asyncio.create_task(self.manual_arm_event.wait())

                done, pending = await asyncio.wait(
                    [sleep_task, event_wait_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()
                
                if self.manual_arm_event.is_set():
                    self.manual_arm_event.clear()

                self.next_bully_time = None
                
                # Announce readiness in a specific channel
                notification_channel_id = 163714449503551488
                channel = self.bot.get_channel(notification_channel_id)
                if channel and isinstance(channel, discord.TextChannel):
                    if await self.config.guild(channel.guild).random_bully_enabled():
                        try:
                            await channel.send("I am armed and ready to bully.")
                        except discord.Forbidden:
                            pass # Can't send message, but continue anyway
                
                # Arm the cog to bully the next valid message
                self.armed_for_random_bully = True
                
                # Wait until a message has been bullied, checking every second
                while self.armed_for_random_bully:
                    await asyncio.sleep(1)

            except asyncio.CancelledError:
                self.next_bully_time = None
                break
            except Exception as e:
                print(f"Error in random bully task: {e}")
                self.next_bully_time = None
                # Wait a bit before restarting the loop to avoid spamming errors
                await asyncio.sleep(60)

    async def _schedule_midnight_reset(self):
        """Schedule the role reset to occur at midnight Central Time."""
        await self.bot.wait_until_ready()
        while self == self.bot.get_cog("Bully"):
            try:
                tz = ZoneInfo("America/Chicago")
                now = datetime.datetime.now(tz)
                
                # Calculate time until next midnight
                tomorrow = (now + datetime.timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                seconds_until_midnight = (tomorrow - now).total_seconds()
                
                # Sleep until midnight
                await asyncio.sleep(seconds_until_midnight)
                
                # Reset all users
                await self._reset_all_users()
                print(f"[Bully] Reset all roles and counts at {datetime.datetime.now(ZoneInfo('America/Chicago'))}")
                
                # Sleep a bit to avoid double execution
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Error in midnight reset task: {e}")

    async def _reset_all_users(self):
        """Reset bully count and remove roles from all users at midnight."""
        try:
            for guild in self.bot.guilds:
                class_clown_role_id = await self.config.guild(guild).class_clown_role_id()
                stinky_loser_role_id = await self.config.guild(guild).stinky_loser_role_id()
                
                class_clown_role = guild.get_role(class_clown_role_id) if class_clown_role_id else None
                stinky_loser_role = guild.get_role(stinky_loser_role_id) if stinky_loser_role_id else None
                
                # Reset all users in this guild
                for member in guild.members:
                    if member.bot:  # Skip bots
                        continue
                        
                    user_data = await self.config.user(member).all()
                    if user_data.get("has_class_clown", False) and class_clown_role and class_clown_role in member.roles:
                        try:
                            await member.remove_roles(class_clown_role, reason="Daily reset")
                        except discord.Forbidden:
                            print(f"Failed to remove Class Clown role from {member.name}: Missing permissions")
                        except Exception as e:
                            print(f"Error removing Class Clown role from {member.name}: {e}")
                            
                    if user_data.get("has_stinky_loser", False) and stinky_loser_role and stinky_loser_role in member.roles:
                        try:
                            await member.remove_roles(stinky_loser_role, reason="Daily reset")
                        except discord.Forbidden:
                            print(f"Failed to remove Stinky Loser role from {member.name}: Missing permissions")
                        except Exception as e:
                            print(f"Error removing Stinky Loser role from {member.name}: {e}")
                    
                    # Reset user's data
                    await self.config.user(member).bully_count.set(0)
                    await self.config.user(member).has_class_clown.set(False)
                    await self.config.user(member).has_stinky_loser.set(False)
                    
        except Exception as e:
            print(f"Error in _reset_all_users: {e}")

    async def _handle_bully_consequences(self, channel: discord.TextChannel, target_user: discord.Member):
        """Checks bully counts and assigns roles if thresholds are met."""
        user_data = await self.config.user(target_user).all()
        bully_count = user_data.get("bully_count", 0)
        has_class_clown = user_data.get("has_class_clown", False)
        has_stinky_loser = user_data.get("has_stinky_loser", False)
        
        guild = channel.guild

        # Check for Stinky Loser role
        if bully_count >= 5 and not has_stinky_loser:
            stinky_loser_role_id = await self.config.guild(guild).stinky_loser_role_id()
            if stinky_loser_role_id:
                role = guild.get_role(stinky_loser_role_id)
                if role:
                    try:
                        await target_user.add_roles(role, reason="Bullied 5 times today")
                        await self.config.user(target_user).has_stinky_loser.set(True)
                        await channel.send(random.choice(self.stinky_loser_messages).format(user=target_user.mention))
                    except discord.Forbidden:
                        print(f"Failed to add Stinky Loser role to {target_user.name}: Missing permissions")

        # Check for Class Clown role
        elif bully_count >= 3 and not has_class_clown:
            class_clown_role_id = await self.config.guild(guild).class_clown_role_id()
            if class_clown_role_id:
                role = guild.get_role(class_clown_role_id)
                if role:
                    try:
                        await target_user.add_roles(role, reason="Bullied 3 times today")
                        await self.config.user(target_user).has_class_clown.set(True)
                        await channel.send(random.choice(self.class_clown_messages).format(user=target_user.mention))
                    except discord.Forbidden:
                        print(f"Failed to add Class Clown role to {target_user.name}: Missing permissions")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for messages to perform random bullying."""
        if message.channel.id == 1282854167240773663:
            return
            
        if not self.armed_for_random_bully:
            return
        if not message.guild:
            return
        if not await self.config.guild(message.guild).random_bully_enabled():
            return
        if message.author.bot:
            return
        if not message.content:
            return
        if (await self.bot.get_context(message)).valid:
            return

        # Roll to see if the bully actually happens
        roll = random.randint(1, 20)

        if roll < 18:
            return  # Abort the bully and stay armed for the next message

        # A valid message has been found AND the roll was successful.
        # Consume the "armed" state.
        self.armed_for_random_bully = False
        target_user = message.author

        # Mock the message and send
        mocked_message = self.sarcog_string(message.content)
        try:
            await message.channel.send(mocked_message)
        except discord.Forbidden:
            return  # Can't send message, but the bully attempt is still consumed
            
        # Increment daily and total bully counts for the victim
        daily_bully_count = await self.config.user(target_user).bully_count() + 1
        await self.config.user(target_user).bully_count.set(daily_bully_count)
        
        total_bullied_count = await self.config.user(target_user).times_bullied_total() + 1
        await self.config.user(target_user).times_bullied_total.set(total_bullied_count)
        
        # Check for role assignments
        await self._handle_bully_consequences(message.channel, target_user)

    @commands.group()
    @commands.admin_or_permissions(administrator=True)
    async def bullyset(self, ctx):
        """Configure the bully cog settings."""
        pass

    @bullyset.command()
    async def classclownrole(self, ctx, role: discord.Role):
        """Set the Class Clown role."""
        await self.config.guild(ctx.guild).class_clown_role_id.set(role.id)
        await ctx.send(f"Class Clown role set to {role.name}")

    @bullyset.command()
    async def stinkyloserrole(self, ctx, role: discord.Role):
        """Set the Stinky Loser role."""
        await self.config.guild(ctx.guild).stinky_loser_role_id.set(role.id)
        await ctx.send(f"Stinky Loser role set to {role.name}")

    @bullyset.command(name="random")
    async def bullyset_random(self, ctx, on_off: bool):
        """Enable or disable random bullying in this server."""
        await self.config.guild(ctx.guild).random_bully_enabled.set(on_off)
        status = "enabled" if on_off else "disabled"
        await ctx.send(f"Random bullying has been {status}.")

    @commands.command(aliases=["b"])
    async def bully(self, ctx: commands.Context):
        """Mock the previous message in alternating case."""
        # Get the previous message
        messages = [msg async for msg in ctx.channel.history(limit=2)]
        if len(messages) < 2:
            await ctx.send("No message to mock!")
            return
            
        target_message = messages[1]  # messages[0] is the command itself
        target_user = target_message.author
        
        if target_user.bot:
            await ctx.send("I don't bully bots!")
            return
            
        # Convert the message to alternating case
        if not target_message.content:
            await ctx.send("Nothing to mock!")
            return
            
        mocked_message = self.sarcog_string(target_message.content)
        
        # Increment bully counts for leaderboard
        author_times_bullied_others = await self.config.user(ctx.author).times_bullied_others()
        await self.config.user(ctx.author).times_bullied_others.set(author_times_bullied_others + 1)
        
        target_times_bullied_total = await self.config.user(target_user).times_bullied_total()
        await self.config.user(target_user).times_bullied_total.set(target_times_bullied_total + 1)

        # Increment bully count and check role thresholds
        bully_count = await self.config.user(target_user).bully_count() + 1
        await self.config.user(target_user).bully_count.set(bully_count)
        
        await self._handle_bully_consequences(ctx.channel, target_user)
        
        # Send the mocked message
        await ctx.send(mocked_message)

    @commands.command(aliases=["bb"])
    async def bullyboard(self, ctx, leaderboard_type: str = "victims"):
        """Show the bully leaderboards.
        
        Parameters
        ----------
        leaderboard_type : str, optional
            The leaderboard to show. Can be 'victims' or 'bullies'. Defaults to 'victims'.
        """
        leaderboard_type = leaderboard_type.lower()
        if leaderboard_type not in ["victims", "bullies"]:
            await ctx.send_help(ctx.command)
            return
            
        all_members = ctx.guild.members
        user_stats = []

        if leaderboard_type == "victims":
            title = "🏆 Most Bullied Victims"
            header = "Times Bullied"
            sort_key = "times_bullied_total"
        else: # bullies
            title = "🏆 Top Bullies"
            header = "Times Bullied Others"
            sort_key = "times_bullied_others"

        for member in all_members:
            if member.bot:
                continue
            
            count = await self.config.user(member).get_raw(sort_key, default=0)
            if count > 0:
                user_stats.append({"member": member, "count": count})

        if not user_stats:
            await ctx.send(f"The '{leaderboard_type}' leaderboard is empty.")
            return
            
        sorted_stats = sorted(user_stats, key=lambda x: x['count'], reverse=True)

        embed = discord.Embed(
            title=title,
            color=await ctx.embed_color()
        )
        
        description = "```\n"
        description += f"Rank  Name                 {header.rjust(15)}\n"
        description += "──────────────────────────────────────────\n"
        
        for i, stats in enumerate(sorted_stats[:15], 1):
            member = stats['member']
            name_str = member.name[:20]
            count_str = f"{stats['count']:,}"
            rank_str = f"#{i}"
            
            description += f"{rank_str:<3}  {name_str:<20} {count_str:>15}\n"
        
        description += "```"
        embed.description = description
        
        other_type = "bullies" if leaderboard_type == "victims" else "victims"
        footer_text = f"Also try: {ctx.prefix}bullyboard {other_type}"
        embed.set_footer(text=footer_text)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.admin_or_permissions(administrator=True)
    async def bullyscan(self, ctx: commands.Context):
        """Scans server history to compile bully statistics."""
        await ctx.send(
            "This will reset all bully leaderboard stats and rescan the server history. "
            "This can take a long time. Are you sure you want to proceed? (yes/no)"
        )

        try:
            check = (
                lambda m: m.author == ctx.author
                and m.channel == ctx.channel
                and m.content.lower() in ["yes", "no"]
            )
            reply = await self.bot.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("No response. Scan cancelled.")
            return

        if reply.content.lower() == "no":
            await ctx.send("Scan cancelled.")
            return

        progress_msg = await ctx.send("Starting bully scan...")

        # Reset existing stats
        for member in ctx.guild.members:
            if not member.bot:
                await self.config.user(member).times_bullied_total.set(0)
                await self.config.user(member).times_bullied_others.set(0)

        user_updates = {}
        total_messages_scanned = 0
        bully_commands_found = 0

        for channel in ctx.guild.text_channels:
            try:
                await progress_msg.edit(content=f"Scanning {channel.mention}...")
                previous_message = None
                async for message in channel.history(limit=None, oldest_first=True):
                    total_messages_scanned += 1
                    if total_messages_scanned % 5000 == 0:
                        await progress_msg.edit(content=f"Scanning {channel.mention}... Processed {total_messages_scanned:,} messages")

                    prefixes = await self.bot.get_prefix(message)
                    if isinstance(prefixes, str):
                        prefixes = [prefixes]
                    
                    is_bully_command = any(message.content.startswith(f"{p}bully") or message.content.startswith(f"{p}b ") or message.content == f"{p}b" for p in prefixes)

                    if is_bully_command and previous_message:
                        bully_commands_found += 1
                        bully = message.author
                        victim = previous_message.author

                        if bully.bot or victim.bot:
                            previous_message = message
                            continue
                        
                        # Update bully stats
                        if bully.id not in user_updates:
                            user_updates[bully.id] = {"bullied_others": 0, "bullied_total": 0, "name": bully.name}
                        user_updates[bully.id]["bullied_others"] += 1

                        # Update victim stats
                        if victim.id not in user_updates:
                            user_updates[victim.id] = {"bullied_others": 0, "bullied_total": 0, "name": victim.name}
                        user_updates[victim.id]["bullied_total"] += 1
                    
                    previous_message = message
            except discord.Forbidden:
                continue
            except Exception as e:
                print(f"Error scanning {channel.name}: {e}")
                continue
        
        await progress_msg.edit(content="Applying updates...")
        for user_id, data in user_updates.items():
            user = ctx.guild.get_member(user_id)
            if user:
                await self.config.user(user).times_bullied_others.set(data["bullied_others"])
                await self.config.user(user).times_bullied_total.set(data["bullied_total"])

        summary = (
            f"Bully scan complete!\n"
            f"Messages scanned: {total_messages_scanned:,}\n"
            f"Bully commands found: {bully_commands_found:,}\n"
            f"Users updated: {len(user_updates)}"
        )
        await progress_msg.edit(content=summary)

    @commands.command()
    async def bullyreset(self, ctx: commands.Context, member: discord.Member = None):
        """Resets the daily bully count for a user.

        If no user is specified, it resets your own count.
        This also removes any daily bully-related roles.

        Parameters
        ----------
        member : discord.Member, optional
            The member whose bully count to reset. Defaults to the command author.
        """
        allowed_ids = [194299256750735361, 115290743354032128]
        if ctx.author.id not in allowed_ids:
            return

        target = member or ctx.author

        try:
            # Reset daily count
            await self.config.user(target).bully_count.set(0)

            # Get role IDs
            class_clown_role_id = await self.config.guild(ctx.guild).class_clown_role_id()
            stinky_loser_role_id = await self.config.guild(ctx.guild).stinky_loser_role_id()

            # Remove Class Clown role if present
            if await self.config.user(target).has_class_clown() and class_clown_role_id:
                role = ctx.guild.get_role(class_clown_role_id)
                if role and role in target.roles:
                    await target.remove_roles(role, reason="Bully count reset by admin")
                await self.config.user(target).has_class_clown.set(False)

            # Remove Stinky Loser role if present
            if await self.config.user(target).has_stinky_loser() and stinky_loser_role_id:
                role = ctx.guild.get_role(stinky_loser_role_id)
                if role and role in target.roles:
                    await target.remove_roles(role, reason="Bully count reset by admin")
                await self.config.user(target).has_stinky_loser.set(False)

            if target == ctx.author:
                await ctx.send("Your daily bully count has been reset.")
            else:
                await ctx.send(f"{target.mention}'s daily bully count has been reset.")

        except discord.Forbidden:
            await ctx.send(f"I don't have permission to remove roles from {target.name}.")
        except Exception as e:
            await ctx.send(f"An error occurred while resetting the bully count: {e}")
            print(f"Error in bullyreset: {e}")

    @commands.command()
    async def bullystats(self, ctx: commands.Context, member: discord.Member = None):
        """Shows bully statistics for a user.

        If no user is specified, it shows your own stats.

        Parameters
        ----------
        member : discord.Member, optional
            The member to get stats for. Defaults to the command author.
        """
        target_user = member or ctx.author

        bullied_others_count = await self.config.user(target_user).times_bullied_others()
        been_bullied_count = await self.config.user(target_user).times_bullied_total()

        embed = discord.Embed(
            title=f"Bully Stats for {target_user.name}",
            color=await ctx.embed_color()
        )
        embed.set_thumbnail(url=target_user.display_avatar.url)
        embed.add_field(name="Times Bullied Others", value=f"{bullied_others_count:,}", inline=False)
        embed.add_field(name="Times Been Bullied", value=f"{been_bullied_count:,}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def bullystatus(self, ctx: commands.Context):
        """Displays the status of the random bully feature."""
        allowed_ids = [194299256750735361, 115290743354032128]
        if ctx.author.id not in allowed_ids:
            return

        is_enabled = await self.config.guild(ctx.guild).random_bully_enabled()

        embed = discord.Embed(
            title="Random Bully Status",
            color=await ctx.embed_color()
        )

        enabled_status_text = "Enabled" if is_enabled else "Disabled"
        embed.add_field(name="Random Bully Feature", value=enabled_status_text, inline=False)

        if is_enabled:
            if self.armed_for_random_bully:
                task_status = "Armed and ready to bully the next message."
                color = discord.Color.green()
            elif self.next_bully_time:
                now = datetime.datetime.now(timezone.utc)
                if self.next_bully_time > now:
                    time_remaining = self.next_bully_time - now
                    minutes, seconds = divmod(int(time_remaining.total_seconds()), 60)
                    task_status = f"Next bully will be armed in: **{minutes:02d}:{seconds:02d}**"
                    color = discord.Color.orange()
                else:
                    task_status = "Currently arming... should be ready any second!"
                    color = discord.Color.yellow()
            else:
                task_status = "The random bully task is initializing."
                color = discord.Color.greyple()
            
            embed.add_field(name="Task State", value=task_status, inline=False)
            embed.color = color
        else:
            embed.color = discord.Color.red()

        await ctx.send(embed=embed)

    @commands.command()
    async def bullyarm(self, ctx: commands.Context):
        """Manually arms the random bully feature, skipping the timer."""
        allowed_ids = [194299256750735361, 115290743354032128]
        if ctx.author.id not in allowed_ids:
            return

        if not await self.config.guild(ctx.guild).random_bully_enabled():
            await ctx.send("Random bully is not enabled, so I cannot arm it.")
            return

        if self.armed_for_random_bully:
            await ctx.send("I am already armed.")
            return

        self.manual_arm_event.set()
        await ctx.send("Arming for the next random bully now...")

async def setup(bot):
    """Load the Bully cog."""
    await bot.add_cog(Bully(bot))
