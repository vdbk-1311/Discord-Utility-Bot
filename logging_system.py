import discord
from discord.ext import commands

class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.log_channel = None

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def set_log(self, ctx, channel: discord.TextChannel):

        self.log_channel = channel.id
        await ctx.send("Log channel set.")

    async def send_log(self, guild, embed):

        if self.log_channel:
            channel = guild.get_channel(self.log_channel)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        embed = discord.Embed(
            title="Message Deleted",
            description=message.content,
            color=discord.Color.red()
        )

        await self.send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):

        embed = discord.Embed(
            title="User Banned",
            description=f"{user}",
            color=discord.Color.red()
        )

        await self.send_log(guild, embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))