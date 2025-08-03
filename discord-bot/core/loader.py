import os

async def load_cogs(bot):
    for folder in os.listdir("cogs"):
        for filename in os.listdir(f"cogs/{folder}"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
