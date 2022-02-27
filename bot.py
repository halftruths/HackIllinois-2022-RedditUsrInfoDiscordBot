# bot.py
import os

import discord
from dotenv import load_dotenv
import scraper as scrape

load_dotenv("./.env")
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "r!"


client = discord.Client()


def help_func():
    return

@client.event
async def on_ready():
    print(f'{client.user} We good')

@client.event
async def on_message(message):
    command = message.content.strip().split(" ")
    if (command[0][0:2] == PREFIX):
        command_name = command[1][0:]
        if message.author == client.user:
            return

        if command_name == 'ping':
            await message.channel.send('pong')

        if command_name == 'help':
            embedH = discord.Embed(title="Help Commands", description="Here is a list of commands available with this bot.")
            
            

        if command_name == 's':
            user_as_redditor = scrape.reddit.redditor(command[2][0:2])
            user_info = scrape.UserInfo()
            if (scrape.UserExists(command[2][0:])):
                embedU = discord.Embed(title="User Information", description="")
                help_func()

        if command_name == 'test': 
            await message.channel.send('tester')


client.run(TOKEN)
