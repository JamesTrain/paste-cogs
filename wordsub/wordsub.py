import discord
import random
from redbot.core import commands, Config
from .pcx_lib import type_message

class WordSub(commands.Cog):
    """A cog for making custom letter substitutions."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=974374576)
        
        default_guild = {
            "substitutions": {}
        }
        
        self.config.register_guild(**default_guild)

    @commands.group()
    async def wordsub(self, ctx):
        """Manage word substitutions."""
        pass

    @wordsub.command(name="apply")
    async def wordsub_apply(self, ctx, name: str):
        """Apply a substitution to the previous message."""
        name = name.lower()
        subs = await self.config.guild(ctx.guild).substitutions()
        
        if name not in subs:
            await ctx.send(f"Substitution profile '{name}' not found.")
            return

        messages = [msg async for msg in ctx.channel.history(limit=2)]
        if len(messages) < 2:
            await ctx.send("No message to apply substitution to.")
            return
            
        original_message = messages[1].content
        if not original_message:
            await ctx.send("Previous message has no content.")
            return

        substitution_map = subs[name]
        new_message = "".join(substitution_map.get(char, char) for char in original_message)
        
        await type_message(
            ctx.channel,
            new_message,
            allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False),
        )

    @wordsub.command(name="add")
    async def wordsub_add(self, ctx, name: str, from_char: str, to_char: str):
        """Add or update a substitution rule."""
        name = name.lower()
        async with self.config.guild(ctx.guild).substitutions() as subs:
            if name not in subs:
                subs[name] = {}
            subs[name][from_char] = to_char
        await ctx.send(f"Substitution rule '{from_char}' -> '{to_char}' added to profile '{name}'.")

    @wordsub.command(name="remove")
    async def wordsub_remove(self, ctx, name: str, from_char: str):
        """Remove a substitution rule."""
        name = name.lower()
        async with self.config.guild(ctx.guild).substitutions() as subs:
            if name not in subs or from_char not in subs[name]:
                await ctx.send(f"Rule '{from_char}' not found in profile '{name}'.")
                return
            del subs[name][from_char]
            if not subs[name]:  # if profile is now empty
                del subs[name]
        await ctx.send(f"Substitution rule '{from_char}' removed from profile '{name}'.")

    @wordsub.command(name="delete")
    async def wordsub_delete(self, ctx, name: str):
        """Delete a substitution profile."""
        name = name.lower()
        async with self.config.guild(ctx.guild).substitutions() as subs:
            if name not in subs:
                await ctx.send(f"Substitution profile '{name}' not found.")
                return
            del subs[name]
        await ctx.send(f"Substitution profile '{name}' deleted.")

    @wordsub.command(name="list")
    async def wordsub_list(self, ctx):
        """List all substitution profiles."""
        subs = await self.config.guild(ctx.guild).substitutions()
        if not subs:
            await ctx.send("No substitution profiles have been created for this server.")
            return
        
        profiles = "\n".join(subs.keys())
        await ctx.send(f"Available substitution profiles:\n```\n{profiles}\n```")

    @wordsub.command(name="view")
    async def wordsub_view(self, ctx, name: str):
        """View the rules for a substitution profile."""
        name = name.lower()
        subs = await self.config.guild(ctx.guild).substitutions()
        if name not in subs:
            await ctx.send(f"Substitution profile '{name}' not found.")
            return

        rules = subs[name]
        if not rules:
            await ctx.send(f"Substitution profile '{name}' has no rules.")
            return
            
        formatted_rules = "\n".join(f"'{k}' -> '{v}'" for k, v in rules.items())
        await ctx.send(f"Rules for '{name}':\n```\n{formatted_rules}\n```") 