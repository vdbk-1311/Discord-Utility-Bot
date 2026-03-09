from PIL.Image import msg
import discord
from discord.ext import commands
from flask import ctx

levels = {}

class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):

        sorted_users = sorted(levels.items(), key=lambda x: x[1], reverse=True)

        msg = ""

        for i,(user,level) in enumerate(sorted_users[:10]):
            msg += f"{i+1}. <@{user}> — Level {level}\n"

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description=msg,
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)
        
    @commands.command()
    async def leaderboard(self, ctx):

        self.cursor.execute(
            "SELECT user_id, level, xp FROM levels ORDER BY xp DESC LIMIT 10"
    )

        data = self.cursor.fetchall()

        msg = ""

        for i, row in enumerate(data):

            user = await self.bot.fetch_user(row[0])

            msg += f"{i+1}. {user.name} | Level {row[1]} | XP {row[2]}\n"

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description=msg,
            color=discord.Color.gold()
    )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))