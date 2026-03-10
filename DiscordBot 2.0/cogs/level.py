from discord.ext import commands
import random
from core.database import connect

class Level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        db = await connect()

        xp = random.randint(5,10)

        await db.execute(
        "UPDATE users SET xp = xp + ? WHERE id = ?",
        (xp,message.author.id)
        )

        await db.commit()

async def setup(bot):
    await bot.add_cog(Level(bot))