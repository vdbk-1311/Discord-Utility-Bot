import discord
from discord.ext import commands
import os
import asyncio

TOKEN = "TOKEN_DISCORD_BOT"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print("=================================")
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("=================================")

@bot.event
async def on_ready():

    await bot.tree.sync()

    print(f"Logged in as {bot.user}")
    print("Slash commands synced")
    
async def load_cogs():

    for file in os.listdir("./cogs"):

        if file.endswith(".py"):

            extension = f"cogs.{file[:-3]}"

            try:

                await bot.load_extension(extension)
                print(f"✅ Loaded {extension}")

            except Exception as e:

                print(f"❌ Failed to load {extension}")
                print(e)


async def main():

    async with bot:

        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())

