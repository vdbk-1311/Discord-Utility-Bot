import discord
from discord.ext import commands
from utils.antispam_state import antispam_state
import time

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = {}

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not antispam_state.enabled:
            return

        if antispam_state.is_whitelisted(message):
            return

        user_id = message.author.id
        now = time.time()

        if user_id not in self.user_messages:
            self.user_messages[user_id] = []

        self.user_messages[user_id].append(now)

        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id] if now - t < 5
        ]

        if len(self.user_messages[user_id]) > 5:
            try:
                await message.delete()
            except:
                pass

            await message.channel.send(
                f"{message.author.mention} please stop spamming.",
                delete_after=5
            )


async def setup(bot):
    await bot.add_cog(AutoMod(bot))