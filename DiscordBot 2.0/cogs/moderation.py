import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def kick(self, ctx, member:discord.Member):

        await member.kick()

        await ctx.send(f"{member} kicked")

    @commands.hybrid_command()
    async def ban(self, ctx, member:discord.Member):

        await member.ban()

        await ctx.send(f"{member} banned")

    @commands.hybrid_command()
    async def clear(self, ctx, amount:int):

        await ctx.channel.purge(limit=amount)

async def setup(bot):
    await bot.add_cog(Moderation(bot))