import discord
from discord.ext import commands

class CommandNode:
    def __init__(self, command, back=None):
        self.command = command
        self.back = back

class CommandHistorique:
    def __init__(self):
        self.Historique = {}

    def add_command(self, id_usr, command):
        if id_usr not in self.Historique:
            self.Historique[id_usr] = CommandNode(command)
        else:
            self.Historique[id_usr] = CommandNode(command, self.Historique[id_usr])

    def get_last_command(self, id_usr):
        if id_usr not in self.Historique:
            return None
        return self.Historique[id_usr].command

    def get_all_commands(self, id_usr):
        if id_usr not in self.Historique:
            return []
        commands = []
        node = self.Historique[id_usr]
        while node:
            commands.append(node.command)
            node = node.back
        return commands

    def get_backious_command(self, id_usr):
        if id_usr not in self.Historique:
            return None
        if not self.Historique[id_usr].back:
            return self.Historique[id_usr].command
        self.Historique[id_usr] = self.Historique[id_usr].back
        return self.Historique[id_usr].command

    def get_next_command(self, id_usr):
        if id_usr not in self.Historique:
            return None
        if not self.Historique[id_usr].back:
            return self.Historique[id_usr].command
        if not self.Historique[id_usr].back.back:
            return self.Historique[id_usr].back.command
        self.Historique[id_usr] = self.Historique[id_usr].back
        return self.Historique[id_usr].command

    def clear_Historique(self, id_usr):
        if id_usr in self.Historique:
            self.Historique[id_usr] = None

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents = intents)

Historique = CommandHistorique()

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command()
async def last_cmd(ctx):
    last_command = Historique.get_last_command(ctx.author.id)
    if last_command:
        await ctx.send(f"Your last command was: {last_command}")
    else:
        await ctx.send("You haven't entered any command yet")

@bot.command()
async def all_cmd(ctx):
    all_commands = Historique.get_all_commands(ctx.author.id)
    if all_commands:
        commands_str = "\n".join(all_commands)
        await ctx.send(f"Your command Historique:\n{commands_str}")
    else:
        await ctx.send("You haven't entered any command yet")

@bot.command()
async def back_cmd(ctx):
    backious_command = Historique.get_backious_command(ctx.author.id)
    if backious_command:
        await ctx.send(f"Your backious command was: {backious_command}")
    else:
        await ctx.send("You are already at the beginning of your command Historique")

@bot.command()
async def next_cmd(ctx):
    next_command = Historique.get_next_command(ctx.author.id)
    if next_command:
        await ctx.send(f"Your next command was: {next_command}")
    else:
        await ctx.send("You are already at the ending of your command Historique")

@bot.command()
async def clear_cmd_Historique(ctx):
    Historique.clear_Historique(ctx.author.id)
    await ctx.send("Your command Historique has been cleared")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")
    Historique.add_command(ctx.author.id, "hello")
    
@bot.command()
async def test(ctx):
    await ctx.send("test, world!")
    Historique.add_command(ctx.author.id, "test")
    


bot.run("MTEwNzU3Mjc4OTEwOTU4ODA2OA.G6AbL6.7SeVmIPSt8WDFBc3wrScqFPHw29BIZK4Ntb9ic")
