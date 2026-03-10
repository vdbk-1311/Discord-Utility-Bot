from discord.ext import commands
from core.database import connect
import random

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def balance(self, ctx):

        db = await connect()

        cursor = await db.execute(
        "SELECT money FROM users WHERE id=?",
        (ctx.author.id,)
        )

        row = await cursor.fetchone()

        await ctx.send(f"💰 {row[0]} coins")

    @commands.hybrid_command()
    async def work(self, ctx):

        amount = random.randint(50,150)

        db = await connect()

        await db.execute(
        "UPDATE users SET money = money + ? WHERE id=?",
        (amount,ctx.author.id)
        )

        await db.commit()

        await ctx.send(f"You earned {amount} coins")

async def setup(bot):
    await bot.add_cog(Economy(bot))