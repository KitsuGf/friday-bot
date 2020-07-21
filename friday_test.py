import os
from discord.ext import commands
import csv

# VARS
path = 'tk/tk.txt'  # Path where is the token file.
tk_file = open(path, "r")  # Reader from txt file.
pr_emojis = {
    1: ":bangbang:",
    2: ":exclamation:",
    3: ":grey_exclamation:",
    4: ":question:",
}
reaction_emojis = {
    1: ":thumbsup:",
    2: ":clap:",
    3: ":wave:",
    4: ":notepad_spiral:"
}

task_status_emojis = {
    1: ":white_check_mark:",
    2: ":fingers_crossed:",
    3: "wrench",
    4: ":x:",
    5: ":muscle:"
}


# PATHS
def task_list_path(group_id, list_id):
    return os.path.join(guild_id_path(group_id), list_id + ".txt")


def guild_id_path(group_id):
    return os.path.join(os.getcwd(), "lists", group_id)


bot = commands.Bot(command_prefix='/')  # Define the bot commands with dot prefix.


@bot.command()
async def new_list(ctx, task_list):
    check_id = os.path.isfile(guild_id_path(str(ctx.guild.id)))
    try:
        if not check_id:
            os.mkdir(guild_id_path(str(ctx.guild.id)))
            new_task_file = open(task_list_path(str(ctx.guild.id), task_list), "x")
            new_task_file.close()
            await ctx.channel.send("List **" + str(task_list) + "** created succesfully!  " + reaction_emojis[2])
    except FileExistsError:
        try:
            new_task_file = open(task_list_path(str(ctx.guild.id), task_list), "x")
            new_task_file.close()
            await ctx.channel.send("List **" + str(task_list) + "** created succesfully!  " + reaction_emojis[2])
        except FileExistsError:
            await ctx.channel.send(
                "Sorry , you already have a list called **" + task_list + "**. You can create a new one or delete the old one.")


@bot.command()
async def remove_list(ctx, task_list):
    try:
        os.remove(task_list_path(str(ctx.guild.id), task_list))
        await  ctx.channel.send("The list named " + task_list + " has been succesfully removed!")
    except FileNotFoundError:
        await  ctx.channel.send("There is no list called " + task_list + " in my database.")


bot.run(tk_file.read())
