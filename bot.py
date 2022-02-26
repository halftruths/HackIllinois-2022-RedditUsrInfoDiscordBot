# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv("./.env")
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "r!"


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} We good')

@client.event
async def on_message(message):
    command = message.content.strip().split()
    if (command[0][0:2] == PREFIX):
        command_name = command[0][2:]
        if message.author == client.user:
            return

        if command_name == 'ping':
            await message.channel.send('pong')


    

client.run(TOKEN)