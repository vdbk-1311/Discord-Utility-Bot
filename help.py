import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="help")
    async def help_command(self, ctx):

        embed = discord.Embed(
            title="🤖 Bot Commands",
            description="List of all available commands",
            color=discord.Color.blue()
        )

        for cog_name, cog in self.bot.cogs.items():

            commands_list = []

            for command in cog.get_commands():

                if command.hidden:
                    continue

                commands_list.append(
                    f"`!{command.name}` - {command.help or 'No description'}"
                )

            if commands_list:

                embed.add_field(
                    name=f"📂 {cog_name}",
                    value=" ".join(commands_list),
                    inline=False
                )

        embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))