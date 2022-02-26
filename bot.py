# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv("./.env")
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} We good')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'ping':
        await message.channel.send('pong')

client.run(TOKEN)