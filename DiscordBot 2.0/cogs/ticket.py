import discord
from discord.ext import commands

class TicketView(discord.ui.View):

    @discord.ui.button(label="Create Ticket",style=discord.ButtonStyle.green)

    async def ticket(self,interaction,button):

        guild = interaction.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )

        await channel.send("Support sẽ hỗ trợ bạn.")

        await interaction.response.send_message(
            "Ticket created",
            ephemeral=True
        )

class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ticketpanel(self, ctx):

        await ctx.send(
            "🎫 Create ticket",
            view=TicketView()
        )

async def setup(bot):
    await bot.add_cog(Ticket(bot))