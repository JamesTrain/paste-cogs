# Jail Cog

A Red-DiscordBot cog that allows server administrators to jail users, preventing them from sending messages in the server.

## Features

- **Jail Users**: Prevent specific users from sending messages
- **Release Users**: Remove users from jail
- **Toggle System**: Enable/disable the jail system per server
- **Multiple Users**: Support for jailing multiple users simultaneously
- **List Management**: View all currently jailed users
- **Permission-Based**: Uses Discord permissions for access control

## Commands

### `[p]jail <user>`
Jails a user, preventing them from sending messages.

**Permissions Required**: Manage Messages or Administrator

### `[p]release <user>`
Releases a user from jail, allowing them to send messages again.

**Permissions Required**: Manage Messages or Administrator

### `[p]jail list`
Lists all currently jailed users in the server.

**Permissions Required**: Manage Messages or Administrator

### `[p]jail toggle`
Toggles the jail system on/off for the server.

**Permissions Required**: Administrator

## Setup

1. Load the cog: `[p]load jail`
2. The jail system is enabled by default
3. Use `[p]jail toggle` to disable if needed

## Permissions

- **Manage Messages**: Required to jail/release users and view jailed list
- **Administrator**: Required to toggle the jail system
- **Manage Messages**: Bot needs this permission to delete messages from jailed users

## Data Storage

This cog stores:
- List of jailed user IDs per guild
- Jail system enabled/disabled status per guild

## Author

Daniel Bush, A.K.A. Daddy 