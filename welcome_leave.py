import discord
from discord.ext import commands

class WelcomeLeave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel = None
        self.leave_channel = None

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel):
        self.welcome_channel = channel.id
        await ctx.send("Welcome channel set.")

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def set_leave(self, ctx, channel: discord.TextChannel):
        self.leave_channel = channel.id
        await ctx.send("Leave channel set.")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if self.welcome_channel:
            channel = member.guild.get_channel(self.welcome_channel)

            embed = discord.Embed(
                title="Welcome!",
                description=f"{member.mention} joined the server",
                color=discord.Color.green()
            )

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if self.leave_channel:
            channel = member.guild.get_channel(self.leave_channel)

            embed = discord.Embed(
                title="Member Left",
                description=f"{member.name} left the server",
                color=discord.Color.red()
            )

            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WelcomeLeave(bot))