import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Ensure a 'data' folder exists to store user balances
if not os.path.exists("data"):
    os.makedirs("data")

# Load user balances from a JSON file
def load_balances():
    try:
        with open("data/balances.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user balances to a JSON file
def save_balances(balances):
    with open("data/balances.json", "w") as file:
        json.dump(balances, file)

@bot.event
async def on_ready():
    print("机器人上线了")

@bot.command(name="hi", description="Say hello to the bot")
async def hello(ctx):
    await ctx.send("Hey!")

# Command to check user balance
@bot.command(name="balance", description="Check your balance")
async def balance(ctx):
    balances = load_balances()
    user_id = str(ctx.author.id)
    user_balance = balances.get(user_id, 0)
    await ctx.send(f"Your balance is: {user_balance} coins")

# Command to earn coins
@bot.command(name="earn", description="Earn some coins")
async def earn(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Amount must be greater than 0.")
        return

    balances = load_balances()
    user_id = str(ctx.author.id)
    user_balance = balances.get(user_id, 0)
    user_balance += amount
    balances[user_id] = user_balance
    save_balances(balances)
    await ctx.send(f"You earned {amount} coins. Your balance is now: {user_balance} coins")

# Command to spend coins
@bot.command(name="spend", description="Spend some coins")
async def spend(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Amount must be greater than 0.")
        return

    balances = load_balances()
    user_id = str(ctx.author.id)
    user_balance = balances.get(user_id, 0)

    if user_balance < amount:
        await ctx.send("Insufficient funds.")
    else:
        user_balance -= amount
        balances[user_id] = user_balance
        save_balances(balances)
        await ctx.send(f"You spent {amount} coins. Your balance is now: {user_balance} coins")

# Run the bot
bot.run('MTIxMzU1MjM1ODQ2NzA1MTU1MA.Gp64yC.cgqVNRNc2cIHDDE2OLE-8lAMmJn-klHlad_3ew')
