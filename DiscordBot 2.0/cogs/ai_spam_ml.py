import discord
from discord.ext import commands
import time

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # config
        self.cooldown = 10
        self.enabled = True

        # tracking
        self.user_last_command = {}

        # whitelist
        self.whitelist_users = set()
        self.whitelist_roles = set()

    # ================================
    # CHECK SPAM
    # ================================
    @commands.Cog.listener()
    async def on_command(self, ctx):

        if not self.enabled:
            return

        user_id = ctx.author.id
        now = time.time()

        # whitelist user
        if user_id in self.whitelist_users:
            return

        # whitelist role
        if ctx.guild:
            for role in ctx.author.roles:
                if role.id in self.whitelist_roles:
                    return

        last = self.user_last_command.get(user_id, 0)

        if now - last < self.cooldown:
            try:
                await ctx.reply(
                    f"⏱️ **Spam detected** — wait `{round(self.cooldown - (now-last),1)}s`",
                    delete_after=5
                )
            except:
                pass

            raise commands.CommandOnCooldown(
                commands.Cooldown(1, self.cooldown),
                self.cooldown
            )

        self.user_last_command[user_id] = now

    # ================================
    # COMMANDS
    # ================================

    @commands.hybrid_command(name="antispam")
    @commands.has_permissions(administrator=True)
    async def toggle_antispam(self, ctx, state: str):
        """
        Enable / Disable anti spam
        """

        state = state.lower()

        if state in ["on","enable","true"]:
            self.enabled = True
            await ctx.reply("✅ Anti-Spam **Enabled**")

        elif state in ["off","disable","false"]:
            self.enabled = False
            await ctx.reply("❌ Anti-Spam **Disabled**")

        else:
            await ctx.reply("Usage: `/antispam on` or `/antispam off`")

    # ================================
    # CHANGE COOLDOWN
    # ================================

    @commands.hybrid_command(name="antispam_cooldown")
    @commands.has_permissions(administrator=True)
    async def change_cooldown(self, ctx, seconds: int):

        if seconds < 1:
            return await ctx.reply("Cooldown must be >= 1s")

        self.cooldown = seconds

        await ctx.reply(f"⏱️ Anti-Spam cooldown set to **{seconds}s**")

    # ================================
    # WHITELIST USER
    # ================================

    @commands.hybrid_command(name="antispam_whitelist_user")
    @commands.has_permissions(administrator=True)
    async def whitelist_user(self, ctx, member: discord.Member):

        self.whitelist_users.add(member.id)

        await ctx.reply(f"✅ {member.mention} added to anti-spam whitelist")

    # ================================
    # WHITELIST ROLE
    # ================================

    @commands.hybrid_command(name="antispam_whitelist_role")
    @commands.has_permissions(administrator=True)
    async def whitelist_role(self, ctx, role: discord.Role):

        self.whitelist_roles.add(role.id)

        await ctx.reply(f"✅ Role **{role.name}** added to whitelist")

    # ================================
    # STATUS
    # ================================

    @commands.hybrid_command(name="antispam_status")
    async def antispam_status(self, ctx):

        status = "Enabled" if self.enabled else "Disabled"

        embed = discord.Embed(
            title="Anti-Spam Status",
            color=discord.Color.green()
        )

        embed.add_field(name="Status", value=status)
        embed.add_field(name="Cooldown", value=f"{self.cooldown}s")

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(AntiSpam(bot))