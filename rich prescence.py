import discord
from discord.ext import commands

# Define intents with the messages intent enabled
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

# Create a bot instance with intents
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Set rich presence when the bot is ready
    await bot.change_presence(
        activity=discord.Game(name="made by changcheng967", type=discord.ActivityType.playing)
    )

# Your other bot commands and event handlers go here

# Run the bot
bot.run('MTE1MTY2MTM2NDQxNTMxNTk5OA.GbGg49.P9Q2kL1b7t-Sqbv8FW9MR2MBl4gqtHKT_VOlpQ')
