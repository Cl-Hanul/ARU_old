import discord as ds
from discord import app_commands
from discord.ext import commands

from os import scandir

## https://zephyrus1111.tistory.com/171
def get_dir_size(path='.'):
    total = 0
    with scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total
def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class Other(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="무게",description="아르가 비밀을 알려줘!")
    async def weight(self,interaction:ds.Interaction):
        await interaction.response.send_message(f"# 무게는 `{convert_size(get_dir_size())}` 이었다..!!")
        
    @app_commands.command(name="프사")
    async def profileimage(self,interaction:ds.Interaction,member:ds.Member):
        await interaction.response.send_message(member.avatar.with_size(512))
    
    @app_commands.command(name="핑",description="아르가 반응에 얼마나 뜸들이는지 알 수 있어!")
    async def ping(self,interaction:ds.Interaction):
        await interaction.response.send_message(f"아르가 `{round(self.bot.latency*1000)} ms`만큼 뜸들였어..!!")