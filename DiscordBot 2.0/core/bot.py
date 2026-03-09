import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def load_cogs():

    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

@bot.event
async def setup_hook():
    await load_cogs()

@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")