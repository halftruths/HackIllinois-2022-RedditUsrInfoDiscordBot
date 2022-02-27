# bot.py
from email.mime import image
import os
from traceback import clear_frames

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

class RedditWrapper:
    user_info: scraper.UserInfo
    user_comments_list: list
    user_submissions_list: list

    def __init__(self, username : str):
        user_as_redditor = reddit.redditor(username)
        self.user_comments_list = list(user_as_redditor.comments.new(limit=99)).copy() #Limited to 100 historical submissions by Reddit API
        self.user_submissions_list = list(user_as_redditor.submissions.new(limit=99)).copy() #Limited to 100 historical submissions by Reddit API
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
            embed = discord.Embed(title="Help Commands", description="Here is a list of commands available with this bot: \n r!ping - responds \"pong\" (connection check) \n r!stats <username> - shows basic user statistics \n r!all <username> - shows all data scraped from reddit \n r!popchart <username> - embeds a piechart of the user's upvote distribution \n r!activitychart <username> - embeds a piechart of user's activity distribution \nr!topcomments <username> - shows the user's top five voted comments \nr!topposts <username> - shows the user's top five voted posts")
            await message.channel.send(embed=embed)
            
        if command_name == 's':
            user_as_redditor = scraper.reddit.redditor(command[2][0:2])
            user_info = scraper.UserInfo()
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username)):
                    add_user_to_dict()
                
                embedU = discord.Embed(title="User Information", description="")
                await message.channel.send(embed=embed)

        if command_name == "popchart":
            if (len(command) == 1):
                await message.channel.send("Error: No username inputted.")
                return

            username = command[1]
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username, reddit=reddit)):
                    add_user_to_dict(username)
                else:
                    await message.channel.send("Error: Invalid username inputted.")
            user = username_dict[username]
            distribution = scraper.VoteDistribution()
            distribution.FindVoteDistribution(user.user_comments_list, user.user_submissions_list)
            dist_list, labels = distribution.GetDistributionAsList()
            plot = plt.pie(dist_list[0:5], labels=labels[0:5], shadow=True, autopct='%1.1f%%', startangle=90)
            plt.title("Upvote Distribution")
            plt.savefig("piechart")
            plt.clf()
            embed = make_embed("Top 5 Subreddits by Upvotes", "For u/" + username)
            file = discord.File("piechart.png", filename="image.png")
            await message.channel.send(file=file, embed=embed)


        if command_name == "activitychart":
            if (len(command) == 1):
                await message.channel.send("Error: No username inputted.")
                return

            username = command[1]
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username, reddit=reddit)):
                    add_user_to_dict(username)
                else:
                    await message.channel.send("Error: Invalid username inputted.")
            user = username_dict[username]
            most_subs = scraper.MostActiveSubs()
            most_subs.FindMostActive(user.user_comments_list, user.user_submissions_list)
            subs_list, labels = most_subs.GetActiveSubsAsList()
            plot = plt.pie(subs_list[0:5], labels=labels[0:5], shadow=True, autopct='%1.1f%%', startangle=90)
            plt.title("Post/Reply Distribution")
            plt.savefig("piechart")
            plt.clf()
            embed = make_embed("Top 5 Subreddits by Posts/Replies", "For u/" + username)
            file = discord.File("piechart.png", filename="image.png")
            await message.channel.send(file=file, embed=embed)

        if command_name == "topposts":
            if (len(command) == 1):
                await message.channel.send("Error: No username inputted.")
                return

            username = command[1]
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username, reddit=reddit)):
                    add_user_to_dict(username)
                else:
                    await message.channel.send("Error: Invalid username inputted.")
            user = username_dict[username]
            top_posts = scraper.TopFiveVotedSubmissionsData()
            top_posts.FindFiveMostVotedSubmissions(user.user_submissions_list)
            posts_string = top_posts.GetFiveMostVotedSubmissions()
            embed = make_embed("Top 5 Posts by Upvotes", "For u/" + username)
            embed.add_field(name="Posts:", value=posts_string, inline=False)
            await message.channel.send(embed=embed)



        if command_name == "topcomments":
            if (len(command) == 1):
                await message.channel.send("Error: No username inputted.")
                return
            
            username = command[1]
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username, reddit=reddit)):
                    add_user_to_dict(username)
                else:
                    await message.channel.send("Error: Invalid username inputted.")
            user = username_dict[username]
            top_comms = scraper.TopFiveVotedCommentsData()
            top_comms.FindFiveMostVotedComments(user.user_comments_list)
            comms_string = top_comms.GetFiveMostVotedComments()
            embed = make_embed("Top 5 Comments by Upvotes", "For u/" + username)
            embed.add_field(name="Comments:", value=comms_string, inline=False)
            await message.channel.send(embed=embed)


        if command_name == "all":
            username = command[1]
            if (not is_user_in_dict(username=username)):
                if (scraper.UserExists(username, reddit=reddit)):
                    add_user_to_dict(username)
                else:
                    await message.channel.send("Error: Invalid username inputted.")
            user = username_dict[username]


def is_user_in_dict(username: str):
    return username in username_dict.keys()

def add_user_to_dict(username: str):
    username_dict[username] = RedditWrapper(username)

def make_embed(embed_title, description):
    embed=discord.Embed(title=embed_title, type="rich", description=description,  color=discord.Color.blue())
    embed.set_image(url="attachment://image.png")
    return embed

client.run(TOKEN)
