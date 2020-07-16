import os
from discord.ext import commands

bot = commands.Bot(command_prefix='/')  # Define the bot commands with dot prefix.
path = 'tk/tk.txt'  # Path where is the token file.
tkFile = open(path, "r")  # Reader from txt file.
listPath = "lists/"  # Path where the id of the server and the list will be saved.
thumbsUp = ":thumbsup:"

# Hello command
@bot.command()
async def Hello(ctx):
    await ctx.channel.send("Hola, " + str(
        ctx.author) + " soy F.R.I.D.A.Y, una asistente virtual creada por Kitsu, ¿en que puedo ayudarte?")


# New List command
@bot.command()
# Ctx its context, thats the parameters of the bot.
# Message its the input of the users.
async def newlist(ctx, message):
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    check_id = os.path.isfile(path_id)  # Check if the server ID exist in directory.
    try: # Try to catch the exception about duplicated ID server directory.
        if not check_id: # If not exist the server ID, create a directory.
            os.mkdir(listPath + str(ctx.guild.id))
            try: # Try to catch the exception about duplicated list.txt.
                f = open(listPath + str(ctx.guild.id) + "/" + str(message) + ".txt", "x")
                f.close()
                await ctx.channel.send("Lista **"+str(message)+"** creada! " +thumbsUp)
            except: # Advice to user about duplicated list.
                await ctx.channel.send("Lo siento ya tienes una lista con ese nombre, prueba a borrarla o crear una "
                                       "diferente.")
    except: # This catch the exception about duplicated ID server and just make the listfile.txt.
        try: # Try to catch the exception about duplicated list.txt.
            f = open(listPath + str(ctx.guild.id) + "/" + str(message) + ".txt", "x")
            f.close()
            await ctx.channel.send("Lista **" +str(message)+"** creada! "+thumbsUp)
        except: # Advice to user about duplicated list.
            await ctx.channel.send("Lo siento ya tienes una lista con ese nombre, prueba a borrarla o crear una "
                                   "diferente.")

# Delete List command
@bot.command()
# Ctx its context, thats the parameters of the bot.
# Message its the input of the users.
async def deletelist(ctx, message):
    path_id = str(ctx.guild.id) # Get the ID from the server.
    try: # Try to get the exception if the file dont exist.
        os.remove(listPath+str(path_id)+"/"+str(message)+".txt") # remove list.txt.
        await  ctx.channel.send("Lista borrada") # Bot advice to user that the list its deleted.
    except: # Exception what catch the "File dont exist."
        await  ctx.channel.send("No existe la lista que deseas borrar.") # Advice to user about not existing list.txt.

bot.run(tkFile.read())  # Run bot with the toke extracted from txt file.
