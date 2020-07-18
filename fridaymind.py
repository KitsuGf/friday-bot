import os
from discord.ext import commands

# Some variables
bot = commands.Bot(command_prefix='/')  # Define the bot commands with dot prefix.
path = 'tk/tk.txt'  # Path where is the token file.
tkFile = open(path, "r")  # Reader from txt file.
listPath = "lists/"  # Path where the id of the server and the list will be saved.
thumbsUp = ":thumbsup:"


# TODO make this command usefull.
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
    try:  # Try to catch the exception about duplicated ID server directory.
        if not check_id:  # If not exist the server ID, create a directory.
            os.mkdir(listPath + str(ctx.guild.id)) # Create the directory with the server id.
            f = open(listPath + str(ctx.guild.id) + "/" + str(ctx.guild.id) + ".txt", "x") # Create a default txt.
            f.close() # Close the file.
            try:  # Try to catch the exception about duplicated list.txt.
                f = open(listPath + str(ctx.guild.id) + "/" + str(message) + ".txt", "x") # Create the list txt.
                f.close() # Close the file.
                await ctx.channel.send("Lista **" + str(message) + "** creada! " + thumbsUp)
            except:  # Advice to user about duplicated list.
                await ctx.channel.send("Lo siento ya tienes una lista con ese nombre, prueba a borrarla o crear una "
                                       "diferente.")
    except:  # This catch the exception about duplicated ID server and just make the listfile.txt.
        try:  # Try to catch the exception about duplicated list.txt.
            f = open(listPath + str(ctx.guild.id) + "/" + str(message) + ".txt", "x")
            f.close()
            await ctx.channel.send("Lista **" + str(message) + "** creada! " + thumbsUp)
        except:  # Advice to user about duplicated list.
            await ctx.channel.send("Lo siento ya tienes una lista con ese nombre, prueba a borrarla o crear una "
                                   "diferente.")


# Delete List command
@bot.command()
# Ctx its context, thats the parameters of the bot.
# Message its the input of the users.
async def deletelist(ctx, message):  # Maybe is should change this to removelist
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    try:  # Try to get the exception if the file dont exist.
        os.remove(listPath + str(path_id) + "/" + str(message) + ".txt")  # remove list.txt.
        await  ctx.channel.send("Lista **" + message + "** borrada con exito. " + thumbsUp)  # Bot advice to user that the list its deleted.
    except:  # Exception what catch the "File dont exist."
        await  ctx.channel.send("No existe la lista que deseas borrar.")  # Advice to user about not existing list.txt.


# Add task selecting list to add tasks.
@bot.command()  # TODO Control the exceptions in addtask.
#  Ctx its context, that's the parameters of the bot.
#  args1 its the argument what user say to the bot to selecting a List
# *args select all the words before the args1.
async def addtask(ctx, args1="", *args):
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    check_file = os.path.isfile(listPath + str(path_id) + "/" + args1 + ".txt")

    if not check_file or args1 is "":  # Check if file exist or user spell it write, or just if args1 is none.
        await ctx.channel.send("No existe la lista de tareas o no la has escrito correctamente.")
    else:
        f = open(listPath + str(path_id) + "/" + args1 + ".txt", "a")  # Open the file with the name of args1.
        f_read = open(listPath + str(path_id) + "/" + args1 + ".txt", "r")  # Same to read jump lines.
        line_counts = f_read.read().count('\n') + 1  # Count the '\n' of the file to add a number in the line.
        f.write(str(line_counts) + " " + str(args).replace("(", "").replace("'", "").replace(",", "").replace(")",
                                                                                                              "") + "\n")  # Write the task in the file.
        f.close()  # Close the File Writer.
        await ctx.channel.send("Tarea añadida a la lista **" + args1 + "** " + thumbsUp)  # Bot advice.


# TODO Control the exceptions in show list.
@bot.command()
async def showlist(ctx, arg):
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    f = open(listPath + str(path_id) + "/" + arg + ".txt", "r")
    await ctx.channel.send("```\n" + f.read() + "```")

# TODO make this as Helper. (Complete it ASAP).
@bot.command()
async def chelp(ctx):
    await ctx.channel.send("```css\n/newlist - Create a new list, example: /newlist Testlist \n"
                           "/addtask - Create a new task but you need to specify the list, example: /addtask Testlist TestTask\n"
                           "/deletelist - Remove the List, example: /deletelist Testlist \n"
                           "/showlist - Show the list what you specify, example: /showlist Testlist```")
bot.run(tkFile.read())  # Run bot with the token extracted from txt file.
