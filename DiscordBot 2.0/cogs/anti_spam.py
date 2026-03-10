from discord.ext import commands
import time

class AntiSpam(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.cooldown = 10
        self.users = {}

    @commands.Cog.listener()
    async def on_command(self, ctx):

        now = time.time()

        user = ctx.author.id

        if user in self.users:

            if now - self.users[user] < self.cooldown:

                await ctx.send("Spam detected")
                return

        self.users[user] = now


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))