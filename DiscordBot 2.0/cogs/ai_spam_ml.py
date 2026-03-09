import discord
from discord.ext import commands
from collections import defaultdict
import time
from datetime import timedelta

ADMIN_IDS = {487562926333493249}

class AntiSpam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.user_messages = defaultdict(list)

        # config
        self.TIME_WINDOW = 10
        self.MESSAGE_LIMIT = 5

        # bật / tắt hệ thống
        self.enabled = True


    def bypass(self, member: discord.Member):

        if member.id in ADMIN_IDS:
            return True

        if member.guild_permissions.administrator:
            return True

        return False


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def antispam(self, ctx, mode: str):

        mode = mode.lower()

        if mode == "on":
            self.enabled = True
            await ctx.send("✅ Anti-Spam enabled")

        elif mode == "off":
            self.enabled = False
            await ctx.send("❌ Anti-Spam disabled")

        else:
            await ctx.send("Usage: `!antispam on/off`")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if not message.guild:
            return

        if message.author.bot:
            return

        if not self.enabled:
            return

        if self.bypass(message.author):
            return

        key = (message.guild.id, message.author.id)
        now = time.time()

        self.user_messages[key].append(now)

        self.user_messages[key] = [
            t for t in self.user_messages[key]
            if now - t <= self.TIME_WINDOW
        ]

        if len(self.user_messages[key]) >= self.MESSAGE_LIMIT:

            try:

                await message.channel.send(
                    f"🚫 Spam detected {message.author.mention}",
                    delete_after=5
                )

                await message.author.timeout(
                    timedelta(seconds=30),
                    reason="Spam detected"
                )

            except Exception as e:
                print(e)

            self.user_messages[key].clear()

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
