import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# VARS
path = 'tk/tk.txt'  # Path where is the token file.
tk_file = open(path, "r")  # Reader from txt file.

# Emojis
pr_emojis = {
    1: ":bangbang:",
    2: ":exclamation:",
    3: ":grey_exclamation:",
    4: ":question:",
}
reaction_emojis = {
    "thumb": ":thumbsup:",
    "clap": ":clap:",
    "wave": ":wave:",
    "notepad": ":notepad_spiral:"
}

task_status_emojis = {
    "done": ":white_check_mark:",
    "await": ":fingers_crossed:",
    "fixing": "wrench",
    "cancel": ":x:",
    "onwork": ":muscle:"
}


# PATHS
def task_list_path(group_id, list_id):
    return os.path.join(guild_id_path(group_id), list_id + ".txt")


def guild_id_path(group_id):
    return os.path.join(os.getcwd(), "lists", group_id)


# DATA ACCESS

# PREFIX BOT COMMANDS
bot = commands.Bot(command_prefix='/')


# EVENTS
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return await ctx.channel.send("The command is misspelled or does not exist. "
                                      "If you need help, use the command **/help_me** please.")
    raise error


@bot.event
async def on_ready():
    # BOT STATUS
    await bot.change_presence(activity=discord.Game(name="/help_me"))


# COMMANDS
@bot.command()
async def new_list(ctx, task_list):
    check_id = os.path.isfile(guild_id_path(str(ctx.guild.id)))
    try:
        if not check_id:
            os.mkdir(guild_id_path(str(ctx.guild.id)))
            new_task_file = open(task_list_path(str(ctx.guild.id), task_list), "x")
            new_task_file.close()
            await ctx.channel.send("List **" + str(task_list) + "** created succesfully!  " + reaction_emojis["clap"])
    except FileExistsError:
        try:
            new_task_file = open(task_list_path(str(ctx.guild.id), task_list), "x")
            new_task_file.close()
            await ctx.channel.send("List **" + str(task_list) + "** created succesfully!  " + reaction_emojis["clap"])
        except FileExistsError:
            await ctx.channel.send(
                "Sorry, you already have a list called **" + task_list + "**. You can create a new one or delete the old one.")


@bot.command()
async def remove_list(ctx, task_list):
    try:
        os.remove(task_list_path(str(ctx.guild.id), task_list))
        await  ctx.channel.send("The list named " + task_list + " has been succesfully removed!")
    except FileNotFoundError:
        await  ctx.channel.send("There is no list called " + task_list + " in my database.")


@bot.command()
async def help_me(ctx):
    await ctx.channel.send("```css\n/new_list - Create a new list, example: /new_list Testlist \n"
                           "/add_task - Create a new task but you need to specify the list, example: /addtask Testlist TestTask\n"
                           "/remove_list - Remove the List, example: /remove_list Testlist \n"
                           "/show_list - Show the list what you specify, example: /show_list Testlist```")


# BOT RUNNING WITH TOKEN.
bot.run(tk_file.read())
