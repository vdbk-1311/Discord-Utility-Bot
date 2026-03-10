import discord
from discord.ext import commands
import os

TOKEN = "MTQ3OTU2OTQ3NzY2MTM2MDMxOA.GLa5OY.1a_tFbxqvP7oCD6L4JrwE4vUKtqQ-Trx493Eco"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def load_cogs():

    for file in os.listdir("./cogs"):

        if file.endswith(".py"):

            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"Loaded {file}")

            except Exception as e:
                print(f"Failed {file}: {e}")

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    await load_cogs()

    await bot.tree.sync()

def start_bot():

    bot.run(TOKEN)