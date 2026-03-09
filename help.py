import discord
from discord.ext import commands
from discord import app_commands


class HelpDropdown(discord.ui.Select):

    def __init__(self, bot):

        self.bot = bot

        options = []

        for cog_name, cog in bot.cogs.items():

            commands_list = [
                cmd for cmd in cog.get_commands()
                if not cmd.hidden
            ]

            if commands_list:

                options.append(
                    discord.SelectOption(
                        label=cog_name,
                        description=f"Commands in {cog_name}",
                        emoji="📂"
                    )
                )

        super().__init__(
            placeholder="Select a command category",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        cog = self.bot.get_cog(self.values[0])

        embed = discord.Embed(
            title=f"📂 {self.values[0]} Commands",
            color=discord.Color.blue()
        )

        for command in cog.get_commands():

            if command.hidden:
                continue

            embed.add_field(
                name=f"/{command.name}",
                value=command.help or "No description",
                inline=False
            )

        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=60)
        self.add_item(HelpDropdown(bot))


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="help",
        description="Show the help menu"
    )
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🤖 Bot Help Menu",
            description="Select a category below",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            embed=embed,
            view=HelpView(self.bot)
        )


async def setup(bot):
    await bot.add_cog(Help(bot))
