import discord
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.author.bot:
            return

        print(f"[DELETE] {message.author} : {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.author.bot:
            return

        print(f"[EDIT] {before.author} : {before.content} -> {after.content}")


async def setup(bot):
    await bot.add_cog(Logging(bot))