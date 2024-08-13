import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Ready for use!")
    print("--------------")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

async def Load():
    for filename in os.listdir("DiscordBot/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await Load()
        await bot.start(TOKEN)

asyncio.run(main())