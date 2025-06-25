import discord
import datetime
import random
from zoneinfo import ZoneInfo
from discord.ext import tasks
from redbot.core import commands, Config

class Bully(commands.Cog):
    """A cog that bullies users by mocking their messages and assigns roles based on bully count."""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374575)
        
        # Default configurations
        default_guild = {
            "class_clown_role_id": None,  # Role ID for Class Clown
            "stinky_loser_role_id": None  # Role ID for Stinky Loser
        }
        default_user = {
            "bully_count": 0,  # Number of times bullied today
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
        
        # Start the midnight reset task
        self.midnight_reset.start()

    def cog_unload(self):
        """Clean up when cog is unloaded."""
        self.midnight_reset.cancel()

    @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=ZoneInfo("America/Chicago")))
    async def midnight_reset(self):
        """Reset all roles at midnight Central Time."""
        try:
            await self._reset_all_users()
            print(f"[Bully] Reset all roles and counts at {datetime.datetime.now(ZoneInfo('America/Chicago'))}")
        except Exception as e:
            print(f"Error in midnight reset task: {e}")

    @midnight_reset.before_loop
    async def before_midnight_reset(self):
        """Wait until the bot is ready before starting the task."""
        await self.bot.wait_until_ready()

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
                    await self.config.user(member).clear()
                    await self.config.user(member).bully_count.set(0)
                    await self.config.user(member).has_class_clown.set(False)
                    await self.config.user(member).has_stinky_loser.set(False)
                    
        except Exception as e:
            print(f"Error in _reset_all_users: {e}")

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

    @commands.command(aliases=["b"])
    async def bully(self, ctx: commands.Context):
        """Mock the previous message in sPoNgEbObCaSe."""
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
            
        # Convert the message to sPoNgEbObCaSe
        if not target_message.content.strip():
            await ctx.send("Nothing to mock!")
            return
            
        mocked_message = "".join(random.choice([c.lower(), c.upper()]) for c in target_message.content)
        
        # Increment bully count and check role thresholds
        user_data = await self.config.user(target_user).all()
        bully_count = user_data.get("bully_count", 0) + 1
        has_class_clown = user_data.get("has_class_clown", False)
        has_stinky_loser = user_data.get("has_stinky_loser", False)
        
        await self.config.user(target_user).bully_count.set(bully_count)
        
        # Check for role assignments
        if bully_count >= 5 and not has_stinky_loser:
            stinky_loser_role_id = await self.config.guild(ctx.guild).stinky_loser_role_id()
            if stinky_loser_role_id:
                role = ctx.guild.get_role(stinky_loser_role_id)
                if role:
                    try:
                        await target_user.add_roles(role, reason="Bullied 5 times today")
                        await self.config.user(target_user).has_stinky_loser.set(True)
                        await ctx.send(random.choice(self.stinky_loser_messages).format(user=target_user.mention))
                    except discord.Forbidden:
                        print(f"Failed to add Stinky Loser role to {target_user.name}: Missing permissions")
                        
        elif bully_count >= 3 and not has_class_clown:
            class_clown_role_id = await self.config.guild(ctx.guild).class_clown_role_id()
            if class_clown_role_id:
                role = ctx.guild.get_role(class_clown_role_id)
                if role:
                    try:
                        await target_user.add_roles(role, reason="Bullied 3 times today")
                        await self.config.user(target_user).has_class_clown.set(True)
                        await ctx.send(random.choice(self.class_clown_messages).format(user=target_user.mention))
                    except discord.Forbidden:
                        print(f"Failed to add Class Clown role to {target_user.name}: Missing permissions")
        
        # Send the mocked message
        await ctx.send(mocked_message)

async def setup(bot):
    """Load the Bully cog."""
    await bot.add_cog(Bully(bot))
