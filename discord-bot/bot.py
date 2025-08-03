import discord
from discord.ext import commands
from config.settings import TOKEN
from core.loader import load_cogs

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
        await load_cogs(bot)

        bot.run(TOKEN)
    