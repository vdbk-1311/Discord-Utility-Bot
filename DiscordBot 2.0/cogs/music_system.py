import discord
from discord.ext import commands
import yt_dlp
import asyncio

class MusicSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    def get_queue(self, guild):
        if guild.id not in self.queue:
            self.queue[guild.id] = []
        return self.queue[guild.id]

    @commands.command()
    async def play(self, ctx, *, query):

        if not ctx.author.voice:
            return await ctx.send("Join a voice channel first.")

        channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await channel.connect()

        ydl = yt_dlp.YoutubeDL({'format': 'bestaudio'})
        info = ydl.extract_info(query, download=False)

        url = info['url']
        title = info['title']

        queue = self.get_queue(ctx.guild)
        queue.append((url, title))

        await ctx.send(f"🎵 Added to queue: **{title}**")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):

        queue = self.get_queue(ctx.guild)

        if not queue:
            return

        url, title = queue.pop(0)

        vc = ctx.voice_client

        vc.play(
            discord.FFmpegPCMAudio(url),
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop
            )
        )

        await ctx.send(f"▶ Now playing: **{title}**")

    @commands.command()
    async def queue(self, ctx):

        queue = self.get_queue(ctx.guild)

        if not queue:
            return await ctx.send("Queue empty")

        msg = "\n".join([f"{i+1}. {song[1]}" for i, song in enumerate(queue)])

        await ctx.send(f"📜 Queue:\n{msg}")

    @commands.command()
    async def skip(self, ctx):

        ctx.voice_client.stop()
        await ctx.send("⏭ Skipped")

    @commands.command()
    async def stop(self, ctx):

        ctx.voice_client.stop()
        self.queue[ctx.guild.id] = []

        await ctx.send("⏹ Stopped music")

async def setup(bot):
    await bot.add_cog(Music(bot))
