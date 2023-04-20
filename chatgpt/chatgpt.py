import discord
import openai
from redbot.core import commands

class ChatGPT(commands.Cog):
    def __init__(self, bot, api_key):
        self.bot = bot
        self.api_key = api_key
        openai.api_key = self.api_key

    @commands.command(name="chatgpt")
    async def chat_gpt(self, ctx, *, prompt: str):
        """
        Sends a prompt to the OpenAI API and receives a response.
        """
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )

            await ctx.send(f"Response from OpenAI API: {response.choices[0].text.strip()}")

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

def setup(bot):
    api_key = bot.get_cog("Config").get_conf(None, identifier=1234567890).get_raw("OPENAI_API_KEY")
    bot.add_cog(ChatGPT(bot, api_key))