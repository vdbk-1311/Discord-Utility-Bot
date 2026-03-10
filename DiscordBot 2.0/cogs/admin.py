from discord.ext import commands
import config

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.is_owner()
    async def reload(self, ctx, cog):

        await self.bot.reload_extension(f"cogs.{cog}")
        await ctx.send(f"Reloaded {cog}")

    @commands.hybrid_command()
    @commands.is_owner()
    async def shutdown(self, ctx):

        await ctx.send("Shutting down...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Admin(bot))