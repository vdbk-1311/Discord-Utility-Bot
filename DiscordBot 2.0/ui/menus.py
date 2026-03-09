import discord

class RoleMenu(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(label="Gamer"),
            discord.SelectOption(label="Music"),
            discord.SelectOption(label="Anime")
        ]

        super().__init__(
            placeholder="Choose role",
            options=options
        )

    async def callback(self,interaction):

        role = discord.utils.get(
            interaction.guild.roles,
            name=self.values[0]
        )

        await interaction.user.add_roles(role)

class SimpleMenu(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(label="Option 1"),
            discord.SelectOption(label="Option 2")
        ]

        super().__init__(
            placeholder="Choose",
            options=options
        )

    async def callback(self,interaction):

        await interaction.response.send_message(
            f"You chose {self.values[0]}",
            ephemeral=True
        )