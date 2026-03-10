import discord

class TicketButton(discord.ui.View):

    @discord.ui.button(label="Create Ticket",style=discord.ButtonStyle.green)
    async def create_ticket(self,interaction,button):

        guild = interaction.guild

        channel = await guild.create_text_channel(
        f"ticket-{interaction.user.name}"
        )

        await channel.send(
        f"{interaction.user.mention} support will help you"
        )

        await interaction.response.send_message(
        "ticket created",
        ephemeral=True
        )
    
    @discord.ui.button(label="Confirm",style=discord.ButtonStyle.green)

    async def confirm(self,interaction,button):

        await interaction.response.send_message(
            "Confirmed!",
            ephemeral=True
        )