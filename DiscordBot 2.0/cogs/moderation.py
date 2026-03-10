import discord
from discord.ext import commands
from utils.antispam_state import antispam_state


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def antispam(self, ctx, mode: str):

        if mode.lower() == "enable":
            antispam_state.enabled = True
            await ctx.send("✅ AntiSpam enabled")

        elif mode.lower() == "disable":
            antispam_state.enabled = False
            await ctx.send("❌ AntiSpam disabled")

    @commands.command()
    async def whitelist_user(self, ctx, member: discord.Member):

        antispam_state.whitelist_users.add(member.id)
        await ctx.send(f"✅ {member} added to whitelist")

    @commands.command()
    async def whitelist_role(self, ctx, role: discord.Role):

        antispam_state.whitelist_roles.add(role.id)
        await ctx.send(f"✅ {role.name} role whitelisted")

    @commands.command()
    async def whitelist_channel(self, ctx, channel: discord.TextChannel):

        antispam_state.whitelist_channels.add(channel.id)
        await ctx.send(f"✅ {channel.mention} channel whitelisted")


async def setup(bot):
    await bot.add_cog(Moderation(bot))