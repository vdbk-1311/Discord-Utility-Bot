import random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coin(self, ctx):

        await ctx.send(random.choice(["Heads", "Tails"]))

    @commands.command()
    async def dice(self, ctx):

        await ctx.send(f"🎲 {random.randint(1,6)}")

async def setup(bot):
    await bot.add_cog(Fun(bot))