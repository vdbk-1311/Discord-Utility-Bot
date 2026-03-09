from discord.ext import commands
from ai.spam_detector import is_spam

class Automod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if is_spam(message.content):

            await message.delete()

            await message.channel.send(
                f"{message.author.mention} spam detected"
            )

async def setup(bot):
    await bot.add_cog(Automod(bot))