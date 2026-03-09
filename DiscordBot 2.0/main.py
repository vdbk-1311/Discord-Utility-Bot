import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN not found in .env file")

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# Bot ready event
@bot.event
async def on_ready():
    print("===================================")
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("Bot is ready!")
    print("===================================")

# Load all cogs automatically
async def load_cogs():

    for file in os.listdir("./cogs"):

        if file.endswith(".py"):

            extension = f"cogs.{file[:-3]}"

            try:
                await bot.load_extension(extension)
                print(f"Loaded {extension}")

            except Exception as e:
                print(f"Failed to load {extension}: {e}")

# Main bot runner
async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)


# Start bot
if __name__ == "__main__":
    asyncio.run(main())
