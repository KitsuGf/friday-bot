import os
from discord.ext import commands

# Some variables
bot = commands.Bot(command_prefix='/')  # Define the bot commands with dot prefix.
path = 'tk/tk.txt'  # Path where is the token file.
tkFile = open(path, "r")  # Reader from txt file.
listPath = "lists/"  # Path where the id of the server and the list will be saved.
# Emojis
thumbsUp = ":thumbsup:"
pr_1 = ":bangbang:"
pr_2 = ":exclamation:"
pr_3 = ":grey_exclamation:"
pr_4 = ":question:"


# TODO make this command usefull.
# Hello command
@bot.command()
async def hello(ctx):
    await ctx.channel.send("Hola, " + str(
        ctx.author) + " soy F.R.I.D.A.Y, una asistente virtual creada por Kitsu, ¿en que puedo ayudarte?")


# New List command
@bot.command()
# Ctx its context, thats the parameters of the bot.
# Message its the input of the users.
async def new_list(ctx, message):
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    check_id = os.path.isfile(path_id)  # Check if the server ID exist in directory.
    try:  # Try to catch the exception about duplicated ID server directory.
        if not check_id:  # If not exist the server ID, create a directory.
            os.mkdir(listPath + str(ctx.guild.id))  # Create the directory with the server id.
            f = open(listPath + str(ctx.guild.id) + "/" + str(ctx.guild.id) + ".txt", "x")  # Create a default txt.
            f.close()  # Close the file.
            try:  # Try to catch the exception about duplicated list.txt.
                f = open(listPath + str(ctx.guild.id) + "/" + str(message) + ".txt", "x")  # Create the list txt.
                f.close()  # Close the file.
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
async def delete_list(ctx, message):  # Maybe is should change this to removelist
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    try:  # Try to get the exception if the file dont exist.
        os.remove(listPath + str(path_id) + "/" + str(message) + ".txt")  # remove list.txt.
        await  ctx.channel.send(
            "Lista **" + message + "** borrada con exito. " + thumbsUp)  # Bot advice to user that the list its deleted.
    except:  # Exception what catch the "File dont exist."
        await  ctx.channel.send("No existe la lista que deseas borrar.")  # Advice to user about not existing list.txt.


# Add task selecting list to add tasks.
@bot.command()  # TODO Control the exceptions in addtask.
#  Ctx its context, that's the parameters of the bot.
#  args1 its the argument what user say to the bot to selecting a List
# *args select all the words before the args1.
async def add_task(ctx, args1="", *args):
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    check_file = os.path.isfile(
        listPath + str(path_id) + "/" + args1 + ".txt")  # Check if the server ID exist in directory.

    if not check_file or args1 is "":  # Check if file exist or user spell it write, or just if args1 is none.
        await ctx.channel.send("No existe la lista de tareas o no la has escrito correctamente.")
    else:
        f = open(listPath + str(path_id) + "/" + args1 + ".txt", "a")  # Open the file with the name of args1.
        f_read = open(listPath + str(path_id) + "/" + args1 + ".txt", "r")  # Same to read jump lines.
        line_counts = f_read.read().count('\n') + 1  # Count the '\n' of the file to add a number in the line.
        f.write(str(line_counts) + " - " + str(args).replace("(", "").replace("'", "").replace(",", "").replace(")",
                                                                                                                "") + "*_\n")  # Write the task in the file.
        f.close()  # Close the File Writer.
        await ctx.channel.send("Tarea añadida a la lista **" + args1 + "** " + thumbsUp)  # Bot advice.


# TODO Control the exceptions in show list.
@bot.command()
async def show_list(ctx, arg):
    path_id = str(ctx.guild.id)  # Get the ID from the server.
    f = open(listPath + str(path_id) + "/" + arg + ".txt", "r")  # Open the file from arguments.
    await ctx.channel.send(
        "" + f.read().replace("*_", ""))  # I make some token to change the color of the lines with the replace.

# TODO TO BE COMMENT
@bot.command()
async def add_pr(ctx, tasklist="", num=0, pr=""):
    path_id = str(ctx.guild.id)
    if pr == "p1":
        a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "r")
        list_of_lines = a_file.readlines()

        if '*_' in list_of_lines[num - 1] or pr_2 in list_of_lines[num - 1] or pr_3 in list_of_lines[num - 1] or pr_4 in \
                list_of_lines[num - 1]:
            list_of_lines[num - 1] = str(
                list_of_lines[num - 1].replace("*_", pr_1).replace(pr_2, pr_1).replace(pr_3, pr_1).replace(pr_4, pr_1))
            a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close()

    if pr == "p2":
        a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "r")
        list_of_lines = a_file.readlines()

        if '*_' in list_of_lines[num - 1] or pr_1 in list_of_lines[num - 1] or pr_3 in list_of_lines[num - 1] or pr_4 in \
                list_of_lines[num - 1]:
            list_of_lines[num - 1] = str(
                list_of_lines[num - 1].replace("*_", pr_2).replace(pr_1, pr_2).replace(pr_3, pr_2).replace(pr_4, pr_2))
            a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close()

    if pr == "p3":
        a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "r")
        list_of_lines = a_file.readlines()

        if '*_' in list_of_lines[num - 1] or pr_1 in list_of_lines[num - 1] or pr_2 in list_of_lines[num - 1] or pr_4 in \
                list_of_lines[num - 1]:
            list_of_lines[num - 1] = str(
                list_of_lines[num - 1].replace("*_", pr_3).replace(pr_1, pr_3).replace(pr_2, pr_3).replace(pr_4, pr_3))
            a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close()

    if pr == "p4":
        a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "r")
        list_of_lines = a_file.readlines()

        if '*_' in list_of_lines[num - 1] or pr_1 in list_of_lines[num - 1] or pr_2 in list_of_lines[num - 1] or pr_3 in \
                list_of_lines[num - 1]:
            list_of_lines[num - 1] = str(
                list_of_lines[num - 1].replace("*_", pr_4).replace(pr_1, pr_4).replace(pr_2, pr_4).replace(pr_3, pr_4))
            a_file = open(listPath + str(path_id) + "/" + tasklist + ".txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close()


# TODO make this as Helper. (Complete it ASAP).
@bot.command()
async def friday_help(ctx):
    await ctx.channel.send("```css\n/newlist - Create a new list, example: /newlist Testlist \n"
                           "/addtask - Create a new task but you need to specify the list, example: /addtask Testlist TestTask\n"
                           "/deletelist - Remove the List, example: /deletelist Testlist \n"
                           "/showlist - Show the list what you specify, example: /showlist Testlist```")


bot.run(tkFile.read())  # Run bot with the token extracted from txt file.
