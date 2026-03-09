import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import time
import os

TOKEN = "YOUR_BOT_TOKEN"

ADMIN_IDS = [
487562926333493249
]

intents = discord.Intents.all()

bot = commands.Bot(
command_prefix="!",
intents=intents
)

tree = bot.tree

spam_data = {}
spam_enabled = True

SPAM_LIMIT = 5
SPAM_TIME = 10

# =========================
# READY
# =========================

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Bot online: {bot.user}")

# =========================
# ANTISPAM
# =========================

@bot.event
async def on_message(message):

    global spam_enabled

    if message.author.bot:
        return

    if not spam_enabled:
        await bot.process_commands(message)
        return

    if message.author.id in ADMIN_IDS:
        await bot.process_commands(message)
        return

    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    user = message.author.id
    now = time.time()

    if user not in spam_data:
        spam_data[user] = []

    spam_data[user].append(now)

    spam_data[user] = [
        t for t in spam_data[user]
        if now - t < SPAM_TIME
    ]

    if len(spam_data[user]) > SPAM_LIMIT:

        try:
            await message.channel.send(
                f"🚫 Spam detected from {message.author.mention}"
            )
        except:
            pass

        return

    await bot.process_commands(message)

# =========================
# ANTISPAM COMMAND
# =========================

@tree.command(name="antispam")
@app_commands.describe(mode="on / off / status")

async def antispam(interaction: discord.Interaction, mode:str):

    global spam_enabled

    if interaction.user.id not in ADMIN_IDS:
        await interaction.response.send_message(
            "❌ Admin only",
            ephemeral=True
        )
        return

    if mode == "on":
        spam_enabled = True
        await interaction.response.send_message("✅ AntiSpam enabled")

    elif mode == "off":
        spam_enabled = False
        await interaction.response.send_message("❌ AntiSpam disabled")

    elif mode == "status":
        await interaction.response.send_message(
            f"AntiSpam: {spam_enabled}"
        )

# =========================
# BASIC COMMANDS
# =========================

@tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong {round(bot.latency*1000)}ms"
    )

@tree.command(name="avatar")
async def avatar(interaction: discord.Interaction, user:discord.Member=None):

    user = user or interaction.user

    embed = discord.Embed(
        title=f"{user.name} avatar"
    )

    embed.set_image(url=user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

# =========================
# MODERATION
# =========================

@tree.command(name="clear")
@app_commands.describe(amount="number of messages")

async def clear(interaction: discord.Interaction, amount:int):

    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ Permission denied")
        return

    await interaction.channel.purge(limit=amount)

    await interaction.response.send_message(
        f"🧹 Cleared {amount} messages",
        ephemeral=True
    )

@tree.command(name="kick")
async def kick(interaction: discord.Interaction, member:discord.Member, reason:str="No reason"):

    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ Permission denied")
        return

    await member.kick(reason=reason)

    await interaction.response.send_message(
        f"👢 {member} kicked"
    )

@tree.command(name="ban")
async def ban(interaction: discord.Interaction, member:discord.Member, reason:str="No reason"):

    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ Permission denied")
        return

    await member.ban(reason=reason)

    await interaction.response.send_message(
        f"🔨 {member} banned"
    )

# =========================
# FUN
# =========================

@tree.command(name="roll")
async def roll(interaction: discord.Interaction):

    import random

    num = random.randint(1,100)

    await interaction.response.send_message(
        f"🎲 You rolled {num}"
    )

# =========================
# HELP
# =========================

@tree.command(name="help")

async def help_cmd(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Discord Utility Bot",
        description="Command list"
    )

    embed.add_field(
        name="Utility",
        value="/ping /avatar /userinfo"
    )

    embed.add_field(
        name="Moderation",
        value="/ban /kick /clear"
    )

    embed.add_field(
        name="Music",
        value="/play /skip /stop"
    )

    embed.add_field(
        name="AntiSpam",
        value="/antispam on/off/status"
    )

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
