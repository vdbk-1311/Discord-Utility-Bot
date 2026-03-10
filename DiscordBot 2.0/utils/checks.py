from discord.ext import commands
import config

def is_owner():

    async def predicate(ctx):

        return ctx.author.id == config.OWNER_ID

    return commands.check(predicate)