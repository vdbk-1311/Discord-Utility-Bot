from discord.ext import commands
import discord

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx):

        await ctx.send(f"Pong {round(self.bot.latency*1000)}ms")


    @commands.hybrid_command()
    async def avatar(self, ctx, user: discord.Member = None):

        user = user or ctx.author

        embed = discord.Embed(title=f"{user.name} avatar")
        embed.set_image(url=user.display_avatar.url)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))