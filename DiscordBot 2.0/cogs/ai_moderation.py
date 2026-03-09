import discord
from discord.ext import commands

bad_words = ["spamlink", "badword", "discord.gg/"]

class AIModeration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        msg = message.content.lower()

        for word in bad_words:
            if word in msg:
                await message.delete()

                embed = discord.Embed(
                    title="⚠️ Auto Moderation",
                    description=f"{message.author.mention} your message contained blocked content.",
                    color=discord.Color.red()
                )

                await message.channel.send(embed=embed, delete_after=5)
                return

async def setup(bot):
    await bot.add_cog(AIModeration(bot))