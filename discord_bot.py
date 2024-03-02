import discord
from discord.ext import commands
from peewee import SqliteDatabase, Model, IntegerField, CharField
import random

intents = discord.Intents(
    messages=True,
    guilds=True,
    members=True,
    presences=True,
    message_content=True
)

# Create an instance of the bot
bot = commands.Bot(command_prefix="/")
inter_client = InteractionClient(bot, test_guilds=[12345, 98765])
# If 'test_guilds' param isn't specified, the commands are registered globally.
# Global registration takes up to 1 hour.

@inter_client.slash_command(
    name="hello", # Defaults to the function name
    description="Says hello",
    guild_ids=test_guilds
)
async def hello(inter):
    await inter.reply("Hello!")
# Discord bot token
TOKEN = 'MTIxMTA4OTAwNjQ2NTY0NjU5Mg.Gt9kfP.i5cuKqrWt1PR9y6FmK5FiA-h6bUfGo0Q6-NxXY'

# Set your database file name
DB_FILE = 'economy_database.db'

# Set the currency symbol
CURRENCY_SYMBOL = 'Dollars'

# Database connection
db = SqliteDatabase(DB_FILE)

# Define the User and Item models
class User(Model):
    user_id = IntegerField(unique=True)
    balance = IntegerField(default=0)

    class Meta:
        database = db

class Item(Model):
    name = CharField(unique=True)
    price = IntegerField()

    class Meta:
        database = db

# Define the Lottery model
class Lottery(Model):
    user_id = IntegerField()
    ticket_number = IntegerField()

    class Meta:
        database = db

# Initialize the database
db.connect()
db.create_tables([User, Item, Lottery], safe=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('-------')
    await update_bot_status()

@bot.event
async def on_message(message):
    # Process commands
    await bot.process_commands(message)

    # Ignore messages from the bot itself to prevent infinite loops
    if message.author == bot.user:
        return

@slash.slash(name='ping', description='Check bot latency')
async def ping(ctx: SlashContext):
    try:
        latency = round(bot.latency * 1000)
        await ctx.send(f'Pong! Latency: {latency}ms')
    except Exception as e:
        print(f"An error occurred in the ping command: {e}")

async def update_bot_status():
    await bot.change_presence(activity=discord.Game(name="made by changcheng967"))

@bot.command(name='balance', help='Check your balance')
async def balance(ctx):
    user = get_or_create_user(ctx.author.id)
    await ctx.send(f'Your balance: {user.balance} {CURRENCY_SYMBOL}')

@bot.command(name='shop', help='View available items in the shop')
async def shop(ctx):
    items = Item.select()
    shop_list = '\n'.join([f'{item.name} - {item.price} {CURRENCY_SYMBOL}' for item in items])
    await ctx.send(f'**Shop Items**:\n{shop_list}')

@bot.command(name='buy', help='Buy an item from the shop')
async def buy(ctx, item_name: str):
    user = get_or_create_user(ctx.author.id)
    item = get_item(item_name)

    if item and user.balance >= item.price:
        user.balance -= item.price
        user.save()
        await ctx.send(f'You bought {item.name} for {item.price} {CURRENCY_SYMBOL}! New balance: {user.balance} {CURRENCY_SYMBOL}')
    elif not item:
        await ctx.send('Item not found in the shop')
    else:
        await ctx.send('Insufficient funds')

@bot.command(name='sell', help='Sell an item to the shop')
async def sell(ctx, item_name: str):
    user = get_or_create_user(ctx.author.id)
    item = get_item(item_name)

    if item:
        user.balance += item.price
        user.save()
        await ctx.send(f'You sold {item.name} for {item.price} {CURRENCY_SYMBOL}! New balance: {user.balance} {CURRENCY_SYMBOL}')
    else:
        await ctx.send('Item not found in the shop')

@bot.command(name='lottery', help='Buy a lottery ticket')
async def lottery(ctx):
    user = get_or_create_user(ctx.author.id)
    if user.balance >= 50:  # Assuming lottery ticket price is 50 coins
        user.balance -= 50
        user.save()

        ticket_number = random.randint(1, 100)
        Lottery.create(user_id=user.user_id, ticket_number=ticket_number)

        await ctx.send(f'You bought a lottery ticket with number {ticket_number} for 50 {CURRENCY_SYMBOL}! Good luck!')
    else:
        await ctx.send(f'You need at least 50 {CURRENCY_SYMBOL} to buy a lottery ticket')

def get_or_create_user(user_id):
    user, created = User.get_or_create(user_id=user_id)
    return user

def get_item(item_name):
    try:
        item = Item.get(Item.name == item_name)
        return item
    except Item.DoesNotExist:
        return None

try:
    roblox_pass = Item.get(Item.name == 'Roblox Season Pass')
    roblox_pass.price = 10000000
    roblox_pass.save()

    minecraft_account = Item.get(Item.name == 'Minecraft Java Edition Account')
    minecraft_account.price = 50000000
    minecraft_account.save()

except Item.DoesNotExist:
    # Create items if they don't exist
    Item.create(name='Roblox Season Pass', price=10000000)
    Item.create(name='Minecraft Java Edition Account', price=50000000)

# Run the bot
bot.run(TOKEN)
