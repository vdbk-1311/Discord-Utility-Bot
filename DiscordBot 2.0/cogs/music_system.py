import discord
from discord.ext import commands

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def play(self, ctx, *, query):

        if not ctx.author.voice:
            return await ctx.send("❌ Join a voice channel first")

        channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await channel.connect()

        await ctx.send(f"🎵 Playing: {query}")


    @commands.hybrid_command()
    async def stop(self, ctx):

        if ctx.voice_client:

            await ctx.voice_client.disconnect()
            await ctx.send("⏹ Music stopped")


async def setup(bot):
    await bot.add_cog(Music(bot))