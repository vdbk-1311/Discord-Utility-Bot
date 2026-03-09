import asyncio

class MusicQueue:

    def __init__(self):
        self.queue = asyncio.Queue()

    async def add(self, track):
        await self.queue.put(track)

    async def next(self):
        return await self.queue.get()

    def empty(self):
        return self.queue.empty()