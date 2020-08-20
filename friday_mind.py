import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import csv
from discord.ext.commands import MemberConverter


# TODO Exceptions: Make all the exceptions and error control.


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
path = 'tk/tk.txt'
tk_file = open(path, "r")
path_help_me = 'src/help_me.txt'

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


# METHODS

def add_task_check(pr, status):
    status_list = {"onwork", "done", "cancel", "fixing", "todo", "await"}
    if pr <= 0 or pr > 4 or status not in status_list:
        checker = False
    else:
        checker = True
    return checker


def check_users_guild(author):
    for guild in bot.guilds:
        for author in guild.members:
            checker = True

    return checker


# EVENTS
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return await ctx.channel.send("The command is misspelled or does not exist. "
                                      "If you need help, use the command **/help_me** please.")


@bot.event
async def on_ready():
    # BOT STATUS
    await bot.change_presence(activity=discord.Game(name="/help_me"))
    print("F.R.I.D.A.Y is online.")


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
            await ctx.channel.send("List **" + str(task_list) + "** created successfully!  " + reaction_emojis["clap"])
        except FileExistsError:
            await ctx.channel.send(
                "Sorry, you already have a list called **" + task_list + "**. You can create a new one or delete the old one.")


@bot.command()
async def remove_list(ctx, task_list):
    try:
        os.remove(task_list_path(str(ctx.guild.id), task_list))
        await  ctx.channel.send("The list named " + task_list + " has been successfully removed!")
    except FileNotFoundError:
        await  ctx.channel.send("There's no list called " + task_list + " in my database.")


@bot.command()
async def add_task(ctx, list_id, task, author="No one", pr=3, status="todo"):
    converter = MemberConverter()
    member = await converter.convert(ctx, author)
    if not add_task_check(pr, status):
        await ctx.channel.send(
            "Remember that the **priority** must be between **1** and **4** and the **status** must be choosen between **these**: \n\t"
            "`- todo`\n\t`- await`\n\t`- cancel`\n\t`- done`\n\t`- onwork`\n\t`- fixing`")
    elif check_users_guild(member):
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
        task_list[int(task_id) - 1].priority = int(pr)
        write_task_list(id_group, list_id, task_list)
        await ctx.channel.send("Priority of task **" + task_id + "** edited  successfully! " + reaction_emojis["thumb"])
    except FileNotFoundError:
        await ctx.channel.send("There's no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")
    except ValueError:
        await ctx.channel.send("Error **" + pr + "** is not a number!")


# TODO Author Exception
@bot.command()
async def edit_author(ctx, list_id, task_id, author):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].author = author
        write_task_list(id_group, list_id, task_list)
        await ctx.channel.send("Author of task **" + task_id + "** edited  successfully! " + reaction_emojis["thumb"])
    except FileNotFoundError:
        await ctx.channel.send("There's no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")


# TODO Status Exception
@bot.command()
async def edit_status(ctx, list_id, task_id, status):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].status = status
        write_task_list(id_group, list_id, task_list)
        await ctx.channel.send("Status of task **" + task_id + "** edited  successfully! " + reaction_emojis["thumb"])
    except FileNotFoundError:
        await ctx.channel.send("There's no list with name **" + list_id + "**")
    except IndexError:
        await ctx.channel.send(
            "Task **" + task_id + "** does not exist in list **" + list_id + "**, please check the task number.")


# TODO Task Exception
@bot.command()
async def edit_task(ctx, list_id, task_id, task):
    try:
        id_group = str(ctx.guild.id)
        task_list = read_task_list(id_group, list_id)
        task_list[int(task_id) - 1].name = task
        write_task_list(id_group, list_id, task_list)
        await ctx.channel.send("Task **" + task_id + "** edited  successfully! " + reaction_emojis["thumb"])
    except FileNotFoundError:
        await ctx.channel.send("There's no list with name **" + list_id + "**")
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
        await ctx.channel.send("There's no list with name **" + list_id + "**")


# TODO END THE HELP ME ASAP.
@bot.command()
async def help_me(ctx):
    with open(path_help_me, "r") as file:
        await ctx.channel.send(file.read())


# COMMAND ERRORS
@add_task.error
async def add_task_error_info(ctx, error):
    if isinstance(error, commands.BadArgument):
        if "Converting" in str(error):
            await ctx.channel.send(
                "The chosen priority is not a number, please choose a **number** between **1** and **4**.")
        elif "Member" in str(error):
            await ctx.channel.send(str(error).replace('"', '**') + ".")
    print(error)


# BOT RUNNING WITH TOKEN.
bot.run(tk_file.read())
