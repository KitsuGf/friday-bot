import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.')  # Define the bot commands with dot prefix.
path = 'tk/tk.txt'  # Path where is the token file.
tkFile = open(path, "r")  # Reader from txt file.


# Test command
@bot.command()
async def hi(ctx):
    await ctx.channel.send("Hola, " + str(
        ctx.author) + " soy F.R.I.D.A.Y, una asistente virtual creada por Kitsu, ¿en que puedo ayudarte?")

bot.run(tkFile.read())  # Run bot with the toke extracted from txt file.


