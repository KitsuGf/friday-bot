import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import csv


# MODEL
class Task:
    def __init__(self, id, name, author, priority, status):
        self.id = id
        self.name = name
        self.author = author
        self.priority = priority
        self.status = status

    def __repr__(self):
        return f"Task({self.id}, {self.name}, {self.author}, {self.priority}, {self.status})"


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
    "fixing": ":wrench:",
    "cancel": ":x:",
    "onwork": ":muscle:",
    "todo": ":pencil:"
}


# PATHS
def task_list_path(group_id, list_id):
    return os.path.join(guild_id_path(group_id), list_id + ".tsv")


def guild_id_path(group_id):
    return os.path.join(os.getcwd(), "lists", group_id)


# DATA ACCESS
def format_task_list(task_list):
    task_result = []
    for task in task_list:
        task_result.append(
            f"`{task.id}`: {task.name} - {task.author} - {pr_emojis[task.priority]} {task_status_emojis[task.status]} ")
    return '\n'.join(task_result)


def emoji_check_priority(priority):
    if priority in pr_emojis:
        return pr_emojis[priority]
    else:
        return f"[PR: {priority}]"


def emoji_check_status(status):
    if status in pr_emojis:
        return pr_emojis[status]
    else:
        return f"[ST: {status}]"


def write_task_list(group_id, list_id, task_list):
    with open(task_list_path(guild_id_path(group_id), list_id), "w", newline='\n', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for task in task_list:
            writer.writerow([task.id, task.name, task.author, task.priority, task.status])


def read_task_list(group_id, list_id):
    result = []
    with open(task_list_path(group_id, list_id), "r", newline='\n', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row is not None and len(row) > 0:
                result.append(Task(int(row[0]), row[1], row[2], int(row[3]), row[4]))
    return result


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
        await  ctx.channel.send("The list named " + task_list + " has been successfully removed!")
    except FileNotFoundError:
        await  ctx.channel.send("There is no list called " + task_list + " in my database.")


@bot.command()
async def add_task(ctx, list_id, task, author="No one", pr=3, status="todo"):
    id_group = str(ctx.guild.id)
    task_list = read_task_list(id_group, list_id)
    new_task = Task(len(task_list) + 1, task, author, pr, status)
    task_list.append(new_task)
    write_task_list(id_group, list_id, task_list)


@bot.command()
async def edit_pr(ctx, list_id, task_id, pr):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].priority = pr
        write_task_list(id_group, list_id, task_list)
    except FileNotFoundError:
        await ctx.channel.send("Theres no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")


@bot.command()
async def edit_author(ctx, list_id, task_id, author):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].author = author
        write_task_list(id_group, list_id, task_list)
    except FileNotFoundError:
        await ctx.channel.send("Theres no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")


@bot.command()
async def edit_status(ctx, list_id, task_id, status):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].status = status
        write_task_list(id_group, list_id, task_list)
    except FileNotFoundError:
        await ctx.channel.send("Theres no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")


@bot.command()
async def edit_task(ctx, list_id, task_id, task):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].name = task
        write_task_list(id_group, list_id, task_list)
    except FileNotFoundError:
        await ctx.channel.send("Theres no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")


@bot.command()
async def show_list(ctx, list_id):
    try:
        id_group = str(ctx.guild.id)
        get_list = read_task_list(id_group, list_id)
        await ctx.channel.send(format_task_list(get_list))
    except FileNotFoundError:
        await ctx.channel.send("Theres no list with name **" + list_id + "**")


# TODO END THE HELP ME ASAP.
# TODO TRY TO READ AS FILE.
@bot.command()
async def help_me(ctx):
    # region Long Message of help_me
    await ctx.channel.send("```yaml\n                                                               Commands```"
                           "```css\n/new_list - Create a new list, example: /new_list Testlist \n"
                           "/add_task - Create a new task but you need to specify the list, example: /add_task Testlist \"TestTaskName between quotes always\"\n"
                           "/remove_list - Remove the List, example: /remove_list Testlist \n"
                           "/show_list - Show the list what you specify, example: /show_list Testlist\n"
                           "/edit_task - TBE\n"
                           "/edit_author - TBE\n"
                           "/edit_status - TBE\n"
                           "/edit_pr - TBE```"
                           "```yaml\n                                                             Emoji System```"
                           "```css\nHow works the Priority System?\n"
                           "First of all, you need to use number between 1 and 4 to select the priority of the task.```\n"
                           + "\t" + pr_emojis[1] + " = `1 - Maximum Priority.`\n"
                           + "\t" + pr_emojis[2] + " = `2 - High Priority.`\n"
                           + "\t" + pr_emojis[3] + " = `3 - Medium Priority.`\n"
                           + "\t" + pr_emojis[4] + " = `4 - Low Priority.`\n\n"
                                                   "```css\nHow Works the Status System?\n"
                                                   "Firs of all, you need to know what status exist on the program, there are various keywords to select it.\n"
                                                   "The words are:\n"
                                                   "\t- todo = Means its without status.\n"
                                                   "\t- await = Mean its waiting to be approved.\n"
                                                   "\t- fixing = Means someone its trying to fix some problem.\n"
                                                   "\t- done = Means the task is done. \n"
                                                   "\t- cancel = Means the task its cancelled for some reason.\n"
                                                   "\t- onwork = Means someone its working on it.```\n"
                           + "\t" + task_status_emojis["todo"] + " = `todo`\n"
                           + "\t" + task_status_emojis["await"] + " = `await`\n"
                           + "\t" + task_status_emojis["fixing"] + " = `fixing`\n"
                           + "\t" + task_status_emojis["done"] + " = `done`\n"
                           + "\t" + task_status_emojis["cancel"] + " = `cancel`\n"
                           + "\t" + task_status_emojis["onwork"] + " = `onwork`\n")
    # endregion


# BOT RUNNING WITH TOKEN.
bot.run(tk_file.read())
