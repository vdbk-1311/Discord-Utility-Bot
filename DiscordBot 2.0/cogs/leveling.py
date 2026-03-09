import discord
from discord.ext import commands
import random

xp = {}
levels = {}

class Leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        user = message.author.id

        if user not in xp:
            xp[user] = 0
            levels[user] = 1

        xp[user] += random.randint(5, 15)

        if xp[user] > levels[user] * 100:
            xp[user] = 0
            levels[user] += 1

            await message.channel.send(
                f"🎉 {message.author.mention} leveled up to **{levels[user]}**!"
            )

    @discord.app_commands.command(name="rank", description="Show your level")
    async def rank(self, interaction: discord.Interaction):

        user = interaction.user.id

        user_level = levels.get(user, 1)
        user_xp = xp.get(user, 0)

        embed = discord.Embed(
            title="🏆 Rank",
            color=discord.Color.gold()
        )

        embed.add_field(name="Level", value=user_level)
        embed.add_field(name="XP", value=user_xp)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))