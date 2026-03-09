import discord
from discord.ext import commands
import time
from collections import defaultdict

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # lưu tin nhắn user
        self.user_messages = defaultdict(list)

        # config
        self.TIME_WINDOW = 5      # 5 giây
        self.MESSAGE_LIMIT = 5    # 5 tin nhắn

    def is_admin(self, member: discord.Member):
        return member.guild_permissions.administrator

    def is_mod(self, member: discord.Member):
        mod_roles = ["mod", "moderator", "admin"]
        return any(role.name.lower() in mod_roles for role in member.roles)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if not message.guild:
            return

        # bỏ qua bot
        if message.author.bot:
            return

        # bỏ qua admin
        if self.is_admin(message.author):
            return

        # bỏ qua mod
        if self.is_mod(message.author):
            return

        user_id = message.author.id
        now = time.time()

        self.user_messages[user_id].append(now)

        # chỉ giữ message trong time window
        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id]
            if now - t <= self.TIME_WINDOW
        ]

        if len(self.user_messages[user_id]) >= self.MESSAGE_LIMIT:

            try:
                await message.channel.send(
                    f"🚫 Spam detected from {message.author.mention}",
                    delete_after=5
                )

                await message.author.timeout(
                    discord.utils.utcnow() + discord.timedelta(seconds=30),
                    reason="Spam detected"
                )

            except Exception:
                pass

            # reset
            self.user_messages[user_id].clear()


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
