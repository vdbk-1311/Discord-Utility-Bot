import discord
from discord.ext import commands

class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def rolepanel(self, ctx):

        embed = discord.Embed(
            title="Choose Role"
        )

        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🎮")
        await msg.add_reaction("🎵")

async def setup(bot):
    await bot.add_cog(Roles(bot))