import discord
from discord.ext import commands
import yt_dlp
import asyncio
import random

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": False,
    "quiet": True
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.now_playing = {}
        self.loop = {}
        self.autoplay = {}

    def get_queue(self, guild):
        if guild.id not in self.queue:
            self.queue[guild.id] = []
        return self.queue[guild.id]

    async def join(self, ctx):

        if not ctx.author.voice:
            await ctx.send("❌ Bạn phải vào voice channel trước")
            return None

        channel = ctx.author.voice.channel

        if ctx.voice_client:
            return ctx.voice_client

        return await channel.connect()

    async def play_next(self, ctx):

        guild = ctx.guild
        queue = self.get_queue(guild)

        if self.loop.get(guild.id) and guild.id in self.now_playing:
            queue.insert(0, self.now_playing[guild.id])

        if not queue:
            await ctx.send("📭 Queue trống")
            return

        url, title = queue.pop(0)

        vc = ctx.voice_client

        self.now_playing[guild.id] = (url, title)

        vc.play(
            discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop
            )
        )

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{title}**",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx, *, query):

        vc = await self.join(ctx)
        if not vc:
            return

        if not query.startswith("http"):
            query = f"ytsearch:{query}"

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)

        queue = self.get_queue(ctx.guild)

        # Playlist
        if "entries" in info:

            count = 0

            for entry in info["entries"]:
                if entry:
                    queue.append((entry["url"], entry["title"]))
                    count += 1

            await ctx.send(f"📜 Added playlist ({count} songs)")

        else:

            queue.append((info["url"], info["title"]))

            await ctx.send(f"🎵 Added: **{info['title']}**")

        if not vc.is_playing():
            await self.play_next(ctx)

    @commands.command()
    async def queue(self, ctx):

        queue = self.get_queue(ctx.guild)

        if not queue:
            return await ctx.send("📭 Queue trống")

        msg = ""

        for i, song in enumerate(queue[:10]):
            msg += f"{i+1}. {song[1]}\n"

        embed = discord.Embed(
            title="📜 Music Queue",
            description=msg,
            color=discord.Color.green()
        )

        embed.set_footer(text=f"{len(queue)} songs in queue")

        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):

        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send("❌ Không có nhạc")

        vc.stop()

        await ctx.send("⏭ Skipped")

    @commands.command()
    async def stop(self, ctx):

        vc = ctx.voice_client

        if not vc:
            return

        self.queue[ctx.guild.id] = []

        vc.stop()

        await ctx.send("⏹ Music stopped")

    @commands.command()
    async def shuffle(self, ctx):

        queue = self.get_queue(ctx.guild)

        if not queue:
            return await ctx.send("Queue trống")

        random.shuffle(queue)

        await ctx.send("🔀 Queue shuffled")

    @commands.command()
    async def loop(self, ctx):

        state = not self.loop.get(ctx.guild.id, False)
        self.loop[ctx.guild.id] = state

        if state:
            await ctx.send("🔁 Loop enabled")
        else:
            await ctx.send("➡ Loop disabled")

    @commands.command()
    async def autoplay(self, ctx):

        state = not self.autoplay.get(ctx.guild.id, False)
        self.autoplay[ctx.guild.id] = state

        if state:
            await ctx.send("🎧 Autoplay enabled")
        else:
            await ctx.send("⛔ Autoplay disabled")

    @commands.command()
    async def nowplaying(self, ctx):

        song = self.now_playing.get(ctx.guild.id)

        if not song:
            return await ctx.send("❌ Không có nhạc")

        embed = discord.Embed(
            title="🎶 Now Playing",
            description=f"**{song[1]}**",
            color=discord.Color.orange()
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):

        vc = ctx.voice_client

        if not vc:
            return

        await vc.disconnect()

        await ctx.send("👋 Disconnected")
        
    @commands.command()
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("⏸ Paused")

    @commands.command()
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("▶ Resumed")

    @commands.command()
    async def volume(self, ctx, vol: int):

        vc = ctx.voice_client

        if not vc:
            return await ctx.send("❌ Not playing")

        vc.source.volume = vol / 100
        await ctx.send(f"🔊 Volume set to {vol}%")

async def setup(bot):
    await bot.add_cog(Music(bot))