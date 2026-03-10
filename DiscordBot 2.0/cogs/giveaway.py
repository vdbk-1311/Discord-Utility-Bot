import discord
from discord.ext import commands
import random
import asyncio

class Giveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: int, prize: str):

        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description=f"Prize: {prize}\nReact with 🎉",
            color=discord.Color.gold()
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")

        await asyncio.sleep(duration)

        message = await ctx.channel.fetch_message(message.id)

        users = []
        for reaction in message.reactions:
            if reaction.emoji == "🎉":
                users = await reaction.users().flatten()

        users = [u for u in users if not u.bot]

        if users:
            winner = random.choice(users)

            await ctx.send(f"🎉 Winner: {winner.mention}")

        else:
            await ctx.send("No winner.")


async def setup(bot):
    await bot.add_cog(Giveaway(bot))