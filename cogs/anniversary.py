import discord as ds
from discord import app_commands
from discord.ext import commands

class Anniversary(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot