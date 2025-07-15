import discord
from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import pagify
from typing import List, Optional


class Jail(commands.Cog):
    """
    Jail users to prevent them from sending messages.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)
        self.config.register_guild(
            jailed_users=[],
            enabled=True
        )
    
    @commands.group(invoke_without_command=True)
    @commands.admin_or_permissions(manage_messages=True)
    async def jail(self, ctx, user: discord.Member):
        """
        Jail a user to prevent them from sending messages.
        
        **Arguments:**
        - `user`: The user to jail
        """
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return
        
        # Check if jail is enabled
        enabled = await self.config.guild(ctx.guild).enabled()
        if not enabled:
            await ctx.send("Jail system is currently disabled.")
            return
        
        # Get current jailed users
        jailed_users = await self.config.guild(ctx.guild).jailed_users()
        
        if user.id in jailed_users:
            await ctx.send(f"{user.mention} is already jailed!")
            return
        
        # Add user to jailed list
        jailed_users.append(user.id)
        await self.config.guild(ctx.guild).jailed_users.set(jailed_users)
        
        await ctx.send(f"🔒 {user.mention} has been jailed! They can no longer send messages.")
    
    @jail.command(name="list")
    @commands.admin_or_permissions(manage_messages=True)
    async def jail_list(self, ctx):
        """
        List all currently jailed users.
        """
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return
        
        jailed_users = await self.config.guild(ctx.guild).jailed_users()
        
        if not jailed_users:
            await ctx.send("No users are currently jailed.")
            return
        
        # Get user objects
        user_list = []
        for user_id in jailed_users:
            user = ctx.guild.get_member(user_id)
            if user:
                user_list.append(f"• {user.mention} ({user.name})")
            else:
                user_list.append(f"• Unknown User ({user_id})")
        
        # Paginate if needed
        pages = list(pagify("\n".join(user_list), page_length=1000))
        
        if len(pages) == 1:
            await ctx.send(f"**Jailed Users:**\n{pages[0]}")
        else:
            for i, page in enumerate(pages, 1):
                await ctx.send(f"**Jailed Users (Page {i}/{len(pages)}):**\n{page}")
    
    @jail.command(name="toggle")
    @commands.admin_or_permissions(administrator=True)
    async def jail_toggle(self, ctx):
        """
        Toggle the jail system on/off.
        """
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return
        
        current_state = await self.config.guild(ctx.guild).enabled()
        new_state = not current_state
        
        await self.config.guild(ctx.guild).enabled.set(new_state)
        
        status = "enabled" if new_state else "disabled"
        await ctx.send(f"🔧 Jail system has been **{status}**.")
    
    @commands.command()
    @commands.admin_or_permissions(manage_messages=True)
    async def release(self, ctx, user: discord.Member):
        """
        Release a user from jail.
        
        **Arguments:**
        - `user`: The user to release
        """
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return
        
        # Get current jailed users
        jailed_users = await self.config.guild(ctx.guild).jailed_users()
        
        if user.id not in jailed_users:
            await ctx.send(f"{user.mention} is not currently jailed!")
            return
        
        # Remove user from jailed list
        jailed_users.remove(user.id)
        await self.config.guild(ctx.guild).jailed_users.set(jailed_users)
        
        await ctx.send(f"🔓 {user.mention} has been released from jail!")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Delete messages from jailed users."""
        if not message.guild:
            return
        
        # Check if jail is enabled
        enabled = await self.config.guild(message.guild).enabled()
        if not enabled:
            return
        
        # Check if user is jailed
        jailed_users = await self.config.guild(message.guild).jailed_users()
        
        if message.author.id in jailed_users:
            try:
                await message.delete()
            except discord.Forbidden:
                # Bot doesn't have permission to delete messages
                pass
            except discord.NotFound:
                # Message was already deleted
                pass 