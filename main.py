import discord
from discord.ext import commands,tasks
import os
import asyncio
from itertools import cycle
import logging
bot = commands.Bot(command_prefix="?",intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.default())



bot_statuses = cycle(["Status : Online"])

@tasks.loop(minutes=5)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("Bot Up")
    change_bot_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An Error with Syncing application command has occured: ",e)

@bot.tree.command(name="hello",description="says hello back to person who run the command")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} Hello There")

@bot.command()
async def test(ctx):
    await ctx.send(f"test, {ctx.author.mention}")

with open("token.txt") as file:
    token = file.read()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())