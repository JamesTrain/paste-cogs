import asyncio
from typing import List, Tuple

import discord
from redbot.core import __version__ as redbot_version
from redbot.core.utils import common_filters

async def type_message(
    destination: discord.abc.Messageable, content: str, **kwargs
) -> discord.Message:
    """Simulate typing and sending a message to a destination.
    Will send a typing indicator, wait a variable amount of time based on the length
    of the text (to simulate typing speed), then send the message.
    """
    content = common_filters.filter_urls(content)
    try:
        async with destination.typing():
            await asyncio.sleep(len(content) * 0.01)
            return await destination.send(content=content, **kwargs)
    except discord.HTTPException:
        pass 