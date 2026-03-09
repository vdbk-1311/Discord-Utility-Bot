import discord
from discord.ext import commands
import sqlite3
import random

class Rank(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("levels.db")
        self.cursor = self.db.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            user_id INTEGER,
            xp INTEGER,
            level INTEGER
        )
        """)
        self.db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        xp = random.randint(5,10)

        self.cursor.execute(
            "SELECT xp, level FROM levels WHERE user_id=?",
            (message.author.id,)
        )

        data = self.cursor.fetchone()

        if data is None:

            self.cursor.execute(
                "INSERT INTO levels VALUES (?,?,?)",
                (message.author.id, xp, 1)
            )

        else:

            xp_total = data[0] + xp
            level = data[1]

            if xp_total > level*100:

                level += 1
                await message.channel.send(
                    f"🎉 {message.author.mention} leveled up to {level}"
                )

            self.cursor.execute(
                "UPDATE levels SET xp=?, level=? WHERE user_id=?",
                (xp_total, level, message.author.id)
            )

        self.db.commit()

async def setup(bot):
    await bot.add_cog(Rank(bot))