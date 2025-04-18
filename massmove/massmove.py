import discord

from redbot.core import commands, checks

from typing import Union, List


class Massmove(commands.Cog):
    """Voice channel massmove and masswap commands."""

    def __init__(self, bot):
        self.bot = bot

    async def red_get_data_for_user(self, **kwargs):
        return {}

    async def red_delete_data_for_user(self, **kwargs):
        return

    @checks.mod_or_permissions(move_members=True)
    @commands.group(
        autohelp=False,
        invoke_without_command=True,
        usage="<from channel> <to channel>"
    )
    async def massmove(
        self,
        ctx,
        channel_from: Union[discord.VoiceChannel, discord.StageChannel],
        channel_to: Union[discord.VoiceChannel, discord.StageChannel]
    ):
        """Massmove members from one channel to another.

        To grab the channel easily, mention it with `#!`.

        Arguments:
            - `from channel`: The channel members will get moved from
            - `to channel`: The channel members will get moved to
        """
        await self.move_all_members(ctx, channel_from, channel_to)

    @checks.mod_or_permissions(move_members=True)
    @commands.command(
        usage="<channel 1> <channel 2>"
    )
    async def massxfer(
        self,
        ctx,
        channel_one: Union[discord.VoiceChannel, discord.StageChannel],
        channel_two: Union[discord.VoiceChannel, discord.StageChannel]
    ):
        """Swap all members between two voice channels.

        This command moves all users from channel 1 to channel 2,
        and all users from channel 2 to channel 1 simultaneously.

        To grab the channel easily, mention it with `#!`.

        Arguments:
            - `channel 1`: First channel to swap
            - `channel 2`: Second channel to swap
        """
        await self.swap_all_members(ctx, channel_one, channel_two)

    @checks.mod_or_permissions(move_members=True)
    @massmove.command(
        usage="<from channel>"
    )
    async def afk(self, ctx, channel_from: Union[discord.VoiceChannel, discord.StageChannel]):
        """Massmove members to the AFK channel

        To grab the channel easily, mention it with ``#!``.

        Arguments:
            - `from channel`: The channel members will get moved from
        """
        await self.move_all_members(ctx, channel_from, ctx.guild.afk_channel)

    @checks.mod_or_permissions(move_members=True)
    @massmove.command(
        usage="<to channel>"
    )
    async def me(self, ctx, channel_to: Union[discord.VoiceChannel, discord.StageChannel]):
        """Massmove you and every other member to another channel.

        To grab the channel easily, mention it with ``#!``.

        Arguments:
            - `to channel`: The channel members will get moved to
        """
        voice = ctx.author.voice
        if voice is None:
            return await ctx.send("You have to be in an voice channel to use this command.")
        await self.move_all_members(ctx, voice.channel, channel_to)

    async def move_all_members(self, ctx, channel_from: discord.VoiceChannel, channel_to: discord.VoiceChannel):
        """Internal function for massmoving, massmoves all members to the target channel"""
        plural = True
        member_amount = len(channel_from.members)
        if member_amount == 0:
            return await ctx.send(f"{channel_from.mention} doesn't have any members in it.")
        elif member_amount == 1:
            plural = False
        # Check permissions to ensure a smooth transisition
        if channel_from.permissions_for(ctx.guild.me).move_members is False:
            return await ctx.send(f"I don't have permissions to move members in {channel_from.mention}.")
        if channel_to.permissions_for(ctx.guild.me).move_members is False:
            return await ctx.send(f"I don't have permissions to move members in {channel_to.mention}.")
        # Move the members
        for member in channel_from.members:
            try:
                await member.move_to(channel_to)
            except:
                pass
        await ctx.send(
            f"Done, massmoved {member_amount} member{'s' if plural else ''} from **{channel_from.mention}** to **{channel_to.mention}**."
        )

    async def swap_all_members(self, ctx, channel_one: discord.VoiceChannel, channel_two: discord.VoiceChannel):
        """Internal function for massxfer, swaps all members between the two target channels"""
        # Store member counts for reporting
        ch1_members = len(channel_one.members)
        ch2_members = len(channel_two.members)
        
        # Check if both channels have users to swap
        if ch1_members == 0 and ch2_members == 0:
            return await ctx.send(f"Both {channel_one.mention} and {channel_two.mention} don't have any members in them.")
        
        # Check permissions to ensure a smooth transisition
        if channel_one.permissions_for(ctx.guild.me).move_members is False:
            return await ctx.send(f"I don't have permissions to move members in {channel_one.mention}.")
        if channel_two.permissions_for(ctx.guild.me).move_members is False:
            return await ctx.send(f"I don't have permissions to move members in {channel_two.mention}.")
        
        # Cache members from both channels first to avoid modification during iteration
        ch1_original_members = list(channel_one.members)
        ch2_original_members = list(channel_two.members)
        
        # Track success counts for each direction
        ch1_to_ch2_moved = 0
        ch2_to_ch1_moved = 0
        
        # Move members from channel one to channel two
        for member in ch1_original_members:
            try:
                await member.move_to(channel_two)
                ch1_to_ch2_moved += 1
            except Exception as e:
                print(f"Error moving {member.display_name} from {channel_one.name} to {channel_two.name}: {e}")
        
        # Move members from channel two to channel one
        for member in ch2_original_members:
            try:
                await member.move_to(channel_one)
                ch2_to_ch1_moved += 1
            except Exception as e:
                print(f"Error moving {member.display_name} from {channel_two.name} to {channel_one.name}: {e}")
        
        # Create response message
        ch1_plural = ch1_members != 1
        ch2_plural = ch2_members != 1
        
        response = f"Done! Swapped members between channels:\n"
        
        if ch1_members > 0:
            response += f"• Moved {ch1_to_ch2_moved}/{ch1_members} member{'s' if ch1_plural else ''} from **{channel_one.name}** to **{channel_two.name}**\n"
        
        if ch2_members > 0:
            response += f"• Moved {ch2_to_ch1_moved}/{ch2_members} member{'s' if ch2_plural else ''} from **{channel_two.name}** to **{channel_one.name}**"
        
        await ctx.send(response) 