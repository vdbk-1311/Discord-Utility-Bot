import discord
from discord.ext import commands
import time
from collections import defaultdict
from datetime import timedelta

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ADMIN ID (thêm ID của bạn vào đây)
        self.ADMIN_IDS = {
            487562926333493249  # Admin 1
                                 # Admin 2
        }

        # lưu lịch sử tin nhắn
        self.user_messages = defaultdict(list)

        # config anti spam
        self.TIME_WINDOW = 5
        self.MESSAGE_LIMIT = 5

    def is_admin(self, member: discord.Member):
        return (
            member.id in self.ADMIN_IDS or
            member.guild_permissions.administrator
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if not message.guild:
            return

        # bỏ qua bot
        if message.author.bot:
            return

        # bỏ qua admin ID
        if self.is_admin(message.author):
            return

        user_id = message.author.id
        now = time.time()

        self.user_messages[user_id].append(now)

        # lọc message cũ
        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id]
            if now - t <= self.TIME_WINDOW
        ]

        # detect spam
        if len(self.user_messages[user_id]) >= self.MESSAGE_LIMIT:

            try:
                await message.channel.send(
                    f"🚫 Spam detected from {message.author.mention}",
                    delete_after=5
                )

                # timeout user
                await message.author.timeout(
                    timedelta(seconds=30),
                    reason="Spam detected"
                )

            except Exception as e:
                print(e)

            # reset counter
            self.user_messages[user_id].clear()


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
