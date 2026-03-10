import discord
from discord.ext import commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green, emoji="🎫")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")

        if category is None:
            category = await guild.create_category("Tickets")

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

        await channel.send(f"{interaction.user.mention} support will be with you soon.")
        await interaction.response.send_message("Ticket created!", ephemeral=True)


class TicketSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def ticket_setup(self, ctx):

        embed = discord.Embed(
            title="Support Tickets",
            description="Click the button to create a ticket",
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed, view=TicketView())


    @commands.hybrid_command()
    async def close(self, ctx):
        if ctx.channel.name.startswith("ticket-"):
            await ctx.send("Ticket closing...")
            await ctx.channel.delete()


async def setup(bot):
    await bot.add_cog(TicketSystem(bot))