# bot.py
from email.mime import image
import os

import praw
import discord
from dotenv import load_dotenv
import scraper
import matplotlib.pyplot as plt

load_dotenv("./.env")
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "r!"

reddit = praw.Reddit( #instance of praw reddit for API access
        client_id = os.getenv("CLIENT_ID"),
        client_secret = os.getenv("CLIENT_SECRET"),
        user_agent = os.getenv("USER_AGENT"),
    )

class redditWrapper:
    user_info: scraper.UserInfo
    user_comments_list: list
    user_submissions_list: list

    def __init__(info: scraper.UserInfo):
        user_info = info
        user_as_redditor = reddit.redditor(user_info.name)
        user_comments_list = list(user_as_redditor.comments.new(limit=99)).copy() #Limited to 100 historical submissions by Reddit API
        user_submissions_list = list(user_as_redditor.submissions.new(limit=99)).copy() #Limited to 100 historical submissions by Reddit API
# Dict of usernames to reddit wrapper object
username_dict = dict()

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

        if command_name == 'help':
            embedH = discord.Embed(title="Help Commands", description="Here is a list of commands available with this bot.")
            
        if command_name == 's':
            user_as_redditor = scraper.reddit.redditor(command[2][0:2])
            user_info = scraper.UserInfo()
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username)):
                    add_user_to_dict()
                
                embedU = discord.Embed(title="User Information", description="")
                help_func()

        if command_name == "popchart":
            username = command[1]
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username)):
                    add_user_to_dict()

        if command_name == "activitychart":
            return


def is_user_in_dict(username: str):
    return username_dict.has_key(str)

def add_user_to_dict(user:UserInfo):
    redditWrapper()

def make_embed(embed_title, description):
    embed=discord.Embed(title=embed_title, type="rich", description=description,  color=discord.Color.blue())
    embed.set_image(url="attachment://image.png")
    return embed

client.run(TOKEN)
