# bot.py
from email.mime import image
import os


import discord
from dotenv import load_dotenv
import scraper as scrape
import matplotlib.pyplot as plt

load_dotenv("./.env")
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "r!"


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} We good')

@client.event
async def on_message(message):
    command = message.content.split()
    if (len(command) == 0 or len(command[0]) < 3):
        return
    if (command[0][0:2] == PREFIX):
        command_name = command[0][2:]
        if message.author == client.user:
            return

        if command_name == 'ping':
            await message.channel.send('pong')

        if command_name == 'test':
            plot = plt.pie([10, 80, 10], explode=[0.5, 0, 0.1], labels=["87", "19", "21"], shadow=True, autopct='%1.1f%%', startangle=90)
            plt.title("What's 9 + 10")
            plt.savefig("piechart")
            embed = make_embed("My Fellow Americans", "According to the 2020 US census")
            file = discord.File("piechart.png", filename="image.png")
            await message.channel.send(file=file, embed=embed)


def make_embed(embed_title, description):
    embed=discord.Embed(title=embed_title, type="rich", description=description,  color=discord.Color.blue())
    embed.set_image(url="attachment://image.png")
    return embed

client.run(TOKEN)
