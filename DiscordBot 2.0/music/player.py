import discord
from music.queue import MusicQueue

class MusicPlayer:

    def __init__(self, bot, guild):

        self.bot = bot
        self.guild = guild
        self.queue = MusicQueue()
        self.voice = None
        self.current = None

    async def connect(self, channel):

        if not self.voice:
            self.voice = await channel.connect()

    async def play(self, source):

        self.current = source

        self.voice.play(
            source,
            after=lambda e: self.bot.loop.create_task(self.play_next())
        )

    async def play_next(self):

        if self.queue.empty():
            return

        track = await self.queue.next()

        await self.play(track)