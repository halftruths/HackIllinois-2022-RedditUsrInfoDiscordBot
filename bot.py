import discord
from discord.ext import commands

TOKEN = open(".env.txt","r").readline()
client = commands.Bot(command_prefix = '.')

async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')

client.run(TOKEN)