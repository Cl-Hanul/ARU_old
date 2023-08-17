import discord as ds
from discord.ext import commands

import json

with open('key.json') as file:
    TOKEN = json.load(file)["discord"]["bot"]["token"]

command_prefix = "~"
intents = ds.Intents.all()
bot = commands.Bot(command_prefix=command_prefix,intents=intents)

@bot.event
async def on_ready():
    print('your bot is ready!')

bot.run(TOKEN)