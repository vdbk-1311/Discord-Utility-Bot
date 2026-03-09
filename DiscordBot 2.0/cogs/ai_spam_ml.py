from email.mime import message
from unittest import result

import discord
from discord.ext import commands
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from utils.spam_model import predict

training = [
("free nitro click here", "spam"),
("discord.gg free", "spam"),
("buy cheap crypto", "spam"),
("hello how are you", "ham"),
("this server is cool", "ham"),
("lets play games", "ham")
]

texts = [t[0] for t in training]
labels = [t[1] for t in training]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

class AISpam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        vec = vectorizer.transform([message.content])
        pred = model.predict(vec)[0]

        if pred == "spam":

            await message.delete()

            await message.channel.send(
                f"⚠ Spam detected from {message.author.mention}",
                delete_after=5
            )

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        result = predict(message.content)

        if result == 1:

            await message.delete()

            await message.channel.send(
                f"🚫 Spam detected from {message.author.mention}"
            )
async def setup(bot):
    await bot.add_cog(AISpam(bot))