import discord

def success(msg):

    embed = discord.Embed(
        description=msg,
        color=0x00ff00
    )

    return embed

def error(msg):

    embed = discord.Embed(
        description=msg,
        color=0xff0000
    )

    return embed