import discord
from discord.ext import commands

class MusicControlView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="⏯ Pause/Resume", style=discord.ButtonStyle.primary)
    async def pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):

        vc = interaction.guild.voice_client

        if not vc:
            return await interaction.response.send_message(
                "❌ Bot is not playing music",
                ephemeral=True
            )

        if vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸ Music paused", ephemeral=True)

        else:
            vc.resume()
            await interaction.response.send_message("▶ Music resumed", ephemeral=True)


    @discord.ui.button(label="⏭ Skip", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):

        vc = interaction.guild.voice_client

        if not vc:
            return await interaction.response.send_message(
                "❌ Nothing playing",
                ephemeral=True
            )

        vc.stop()

        await interaction.response.send_message("⏭ Skipped", ephemeral=True)


    @discord.ui.button(label="⏹ Stop", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):

        vc = interaction.guild.voice_client

        if not vc:
            return await interaction.response.send_message(
                "❌ Nothing playing",
                ephemeral=True
            )

        await vc.disconnect()

        await interaction.response.send_message("⏹ Music stopped", ephemeral=True)


class MusicUI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =============================
    # MUSIC PANEL
    # =============================

    @commands.hybrid_command(name="musicpanel")
    async def music_panel(self, ctx):
        """
        Show music control panel
        """

        embed = discord.Embed(
            title="🎵 Music Control Panel",
            description="Use the buttons below to control music",
            color=discord.Color.green()
        )

        embed.add_field(name="Pause/Resume", value="Toggle music")
        embed.add_field(name="Skip", value="Skip current song")
        embed.add_field(name="Stop", value="Stop music")

        await ctx.send(embed=embed, view=MusicControlView(self.bot))

    # =============================
    # NOW PLAYING UI
    # =============================

    @commands.hybrid_command(name="nowplaying")
    async def now_playing(self, ctx):

        vc = ctx.guild.voice_client

        if not vc or not vc.is_playing():

            embed = discord.Embed(
                title="Nothing playing",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="🎶 Now Playing",
            description="Music is currently playing",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=MusicControlView(self.bot))


# =============================
# COG SETUP
# =============================

async def setup(bot):
    await bot.add_cog(MusicUI(bot))