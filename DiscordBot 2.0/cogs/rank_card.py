import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

levels = {}

class RankCard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def rank(self, ctx):

        user = ctx.author

        level = levels.get(user.id, 1)
        xp = level * 100

        avatar = requests.get(user.display_avatar.url).content
        avatar = Image.open(BytesIO(avatar)).resize((128,128))

        img = Image.new("RGB",(600,200),(30,30,30))
        draw = ImageDraw.Draw(img)

        img.paste(avatar,(20,40))

        font = ImageFont.load_default()

        draw.text((180,50),user.name,font=font,fill=(255,255,255))
        draw.text((180,100),f"Level: {level}",font=font,fill=(255,255,255))
        draw.text((180,130),f"XP: {xp}",font=font,fill=(255,255,255))

        img.save("rank.png")

        await ctx.send(file=discord.File("rank.png"))

async def setup(bot):
    await bot.add_cog(RankCard(bot))