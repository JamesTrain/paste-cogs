import discord
import datetime
import asyncio
import random
from redbot.core import commands, Config
from .pcx_lib import type_message

pank = 69420

class bully(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374575)
        default_guild = {
            "class_clown_role_id": 1384978602780524554,  # Role ID for Class Clown
            "stinky_loser_role_id": 1384978809287082116  # Role ID for Stinky Loser
        }
        default_user = {
            "bully_count": 0,  # Number of times bullied today
            "last_reset": None  # Last time the count was reset
        }
        self.config.register_guild(**default_guild)
        self.config.register_user(**default_user)
        
        # Sassy messages for role assignments
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
        
        # Start the background task to check for midnight reset
        self.midnight_task = self.bot.loop.create_task(self._schedule_midnight_reset())

    def cog_unload(self):
        # Cleanup when cog is unloaded
        if self.midnight_task:
            self.midnight_task.cancel()

    async def _schedule_midnight_reset(self):
        """Schedule the role reset to occur at midnight Central Time."""
        await self.bot.wait_until_ready()
        while self == self.bot.get_cog("bully"):
            now = datetime.datetime.now(datetime.timezone.utc)
            # Convert to Central Time
            central = now.astimezone(datetime.timezone(datetime.timedelta(hours=-6)))
            # Calculate time until next midnight CT
            tomorrow = (central + datetime.timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            seconds_until_midnight = (tomorrow - central).total_seconds()
            
            # Sleep until midnight
            await asyncio.sleep(seconds_until_midnight)
            
            # Reset all users
            await self._reset_all_users()
            
            # Sleep a bit to avoid double execution
            await asyncio.sleep(60)

    async def _reset_all_users(self):
        """Reset bully count and remove roles from all users at midnight."""
        for guild in self.bot.guilds:
            class_clown_role_id = await self.config.guild(guild).class_clown_role_id()
            stinky_loser_role_id = await self.config.guild(guild).stinky_loser_role_id()
            
            if class_clown_role_id:
                class_clown_role = guild.get_role(class_clown_role_id)
                if class_clown_role:
                    for member in class_clown_role.members:
                        await member.remove_roles(class_clown_role, reason="Daily reset")
            
            if stinky_loser_role_id:
                stinky_loser_role = guild.get_role(stinky_loser_role_id)
                if stinky_loser_role:
                    for member in stinky_loser_role.members:
                        await member.remove_roles(stinky_loser_role, reason="Daily reset")
            
            # Reset all user counts in this guild
            async for user_id in self.config.all_users():
                member = guild.get_member(user_id)
                if member:
                    await self.config.user(member).bully_count.set(0)
                    await self.config.user(member).last_reset.set(datetime.datetime.now().isoformat())

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
    async def sarcasm(self, ctx: commands.Context):
        #Define the command for RedBot
        messages = [msg async for msg in ctx.channel.history(limit=2)]
        messageObject = messages[1]
        message = messageObject.content
        target_user = messageObject.author
        
        if not message:
            message = "I can't translate that!"
        if messageObject.author.id == pank:
            await type_message(
                ctx.channel,
                self.sarcog_string("Austin is a fucking idiot"),
                allowed_mentions=discord.AllowedMentions(
                    everyone=False, users=False, roles=False),
            )
            return
        
        # Increment bully count for the target user
        bully_count = await self.config.user(target_user).bully_count()
        bully_count += 1
        await self.config.user(target_user).bully_count.set(bully_count)
        
        # Check role thresholds and assign roles
        if bully_count >= 3:
            class_clown_role_id = await self.config.guild(ctx.guild).class_clown_role_id()
            if class_clown_role_id:
                role = ctx.guild.get_role(class_clown_role_id)
                if role and role not in target_user.roles:
                    await target_user.add_roles(role, reason="Bullied 3 times today")
                    # Send a sassy message about Class Clown role
                    sassy_message = random.choice(self.class_clown_messages).format(user=target_user.mention)
                    await ctx.send(sassy_message)
        
        if bully_count >= 5:
            stinky_loser_role_id = await self.config.guild(ctx.guild).stinky_loser_role_id()
            if stinky_loser_role_id:
                role = ctx.guild.get_role(stinky_loser_role_id)
                if role and role not in target_user.roles:
                    await target_user.add_roles(role, reason="Bullied 5 times today")
                    # Send a sassy message about Stinky Loser role
                    sassy_message = random.choice(self.stinky_loser_messages).format(user=target_user.mention)
                    await ctx.send(sassy_message)
        
        await type_message(
            ctx.channel,
            self.sarcog_string(message),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False),
        )
        
    @staticmethod
    def sarcog_string(x):
        #Sarcasm and return string
        output = []
        for let in range(len(x)):
            if let%2==0:
                output.append(x[let].lower())
            else:
                output.append(x[let].upper())
        return "".join(output)
