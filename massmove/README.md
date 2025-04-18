# Massmove Cog for Red Discord Bot

A cog providing voice channel management commands for server moderators.

## Commands

### Massmove

- `[p]massmove <from_channel> <to_channel>` - Move all members from one voice channel to another
- `[p]massmove afk <from_channel>` - Move all members to the server's AFK channel
- `[p]massmove me <to_channel>` - Move you and everyone in your current voice channel to another channel

### Massxfer

- `[p]massxfer <channel_1> <channel_2>` - Swap all members between two voice channels

## Permissions

All commands require the `Move Members` permission.

## Installation

To install this cog, run the following commands in your Red Discord Bot:

```
[p]repo add massmove <repo_url>
[p]cog install massmove
[p]load massmove
```

## License

This cog is licensed under the Mozilla Public License, v. 2.0. 