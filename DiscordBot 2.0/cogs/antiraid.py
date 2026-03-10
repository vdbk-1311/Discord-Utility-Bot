import discord
from discord.ext import commands
import time

class AntiRaid(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.join_times = []

    @commands.Cog.listener()
    async def on_member_join(self, member):

        now = time.time()
        self.join_times.append(now)

        self.join_times = [t for t in self.join_times if now - t < 10]

        if len(self.join_times) > 5:
            channel = member.guild.system_channel

            if channel:
                await channel.send("⚠️ Possible raid detected!")

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))