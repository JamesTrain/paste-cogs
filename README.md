# PasteCogs

A collection of useful cogs for [Red Discord Bot](https://github.com/Cog-Creators/Red-DiscordBot) maintained by The Paste Team.

## Available Cogs

| Cog | Description |
|-----|-------------|
| [Autokick](#autokick) | Automatically kick users based on configured rules |
| [Bully](#bully) | Fun bully/compliment commands |
| [Extremeuwu](#extremeuwu) | Make messages extremely UwU |
| [Lmgtfy](#lmgtfy) | Generate "Let Me Google That For You" links |
| [Massmove](#massmove) | Move or swap members between voice channels |
| [Pastepoints](#pastepoints) | Points/currency system for your server |
| [Ppmonth](#ppmonth) | Profile picture of the month contest tracker |
| [Rmjoey](#rmjoey) | Joey management commands |
| [Vibecheck](#vibecheck) | Check and track your daily vibes |
| [WordSub](#wordsub) | Create custom letter substitutions |

## Installation

To install these cogs, follow these steps:

1. Add the repository to your Red instance:
   ```
   [p]repo add pastecogs https://github.com/JamesTrain/paste-cogs
   ```

2. Install the desired cog:
   ```
   [p]cog install pastecogs <cogname>
   ```

3. Load the cog:
   ```
   [p]load <cogname>
   ```

## Cog Details

### Autokick

Automatically kick users based on configured rules.

Commands:
- `[p]autokick` - Main autokick command group
- `[p]autokick set` - Set up the autokick configuration
- `[p]autokick list` - List current autokick settings

### Bully

Fun commands to bully or compliment other users.

Commands:
- `[p]bully <user>` - Bully a user with a random message
- `[p]compliment <user>` - Compliment a user with a random message

### Extremeuwu

Convert messages to extremely UwU versions.

Commands:
- `[p]uwu <text>` - Convert text to UwU speak
- `[p]extremeuwu <text>` - Convert text to EXTREME UwU speak

### Lmgtfy

Generate "Let Me Google That For You" links.

Commands:
- `[p]lmgtfy <query>` - Generate a LMGTFY link for the given query

### Massmove

Commands to move or swap multiple users between voice channels at once.

Commands:
- `[p]massmove <from_channel> <to_channel>` - Move all members from one voice channel to another
- `[p]massmove afk <from_channel>` - Move all members to the AFK channel
- `[p]massmove me <to_channel>` - Move you and everyone in your current voice channel to another
- `[p]massxfer <channel_1> <channel_2>` - Swap all members between two voice channels

### Pastepoints

A points/currency system for your server.

Commands:
- `[p]points` - Check your points
- `[p]points give <user> <amount>` - Give points to another user
- `[p]points leaderboard` - Show the points leaderboard

### Ppmonth

Profile picture of the month contest tracker.

Commands:
- `[p]ppmonth` - Commands related to Profile Picture of the Month
- `[p]ppmonth submit` - Submit your profile picture to the contest
- `[p]ppmonth vote <user>` - Vote for a user's profile picture

### Rmjoey

Joey management commands.

Commands:
- `[p]joey` - Joey-related commands
- `[p]joeyadd <name>` - Add a new Joey
- `[p]joeylist` - List all Joeys

### Vibecheck

Check your daily vibes and compete with others on the vibe leaderboard.

Commands:
- `[p]vibecheck` - Check your vibes for the day (can only be used once per day)
- `[p]vibestats [user]` - View vibe check statistics for yourself or another user
- `[p]vibeboard [total/avg]` - Show the vibe leaderboard for all users

### WordSub

Create custom letter substitutions that can be applied to messages.

Commands:
- `[p]wordsub apply <name>` - Apply a substitution to the previous message.
- `[p]wordsub add <name> <from_char> <to_char>` - Add or update a substitution rule.
- `[p]wordsub remove <name> <from_char>` - Remove a substitution rule.
- `[p]wordsub delete <name>` - Delete a substitution profile.
- `[p]wordsub list` - List all substitution profiles.
- `[p]wordsub view <name>` - View the rules for a substitution profile.

## Support

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository or contact The Paste Team on Discord.

## License

All cogs in this repository are licensed under the Mozilla Public License, v. 2.0.