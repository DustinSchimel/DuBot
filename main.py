import discord
from discord.ext import commands
import music
from keep_alive import keep_alive
import os
my_secret = os.environ['DISCORD_TOKEN']


cogs = [music]

client = commands.Bot(command_prefix='?', intents = discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client)

keep_alive()
client.run(my_secret)