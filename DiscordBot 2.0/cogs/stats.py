import discord
from discord.ext import commands


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="stats", description="Show bot statistics")
    async def stats(self, interaction: discord.Interaction):

        servers = len(self.bot.guilds)
        users = sum(g.member_count for g in self.bot.guilds)
        ping = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🤖 Bot Statistics",
            color=discord.Color.blue()
        )

        embed.add_field(name="Servers", value=servers)
        embed.add_field(name="Users", value=users)
        embed.add_field(name="Ping", value=f"{ping}ms")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot))