import discord as ds
from discord.ext import commands

class Item(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot