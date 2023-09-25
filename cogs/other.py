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
    
    @app_commands.command(name="수면시간", description="아르가 재워줄게..")
    @app_commands.choices(waketimehour=[app_commands.Choice(name=hour,value=hour) for hour in range(1,25)])
    @app_commands.choices(waketimeminute=[app_commands.Choice(name=minute,value=minute) for minute in range(0,60)])
    async def sleeptime(self, interaction:ds.Interaction, waketimehour:app_commands.Choice[int],waketimeminute:app_commands.Choice[int]):
        waketime = waketimehour.value*60 + waketimeminute.value
        sleeptime = [
            waketime-270-270,
            waketime-270-180,
            waketime-270-90,
            waketime-270
        ]
        one2two = lambda num: f"{num}" if len(str(num)) > 1 else f"0{num}"
        minute2time = lambda minute: f"{one2two(minute//60)}:{one2two(minute%60)}" if minute >= 0 else f"{one2two((1440+minute)//60)}:{one2two((1440+minute)%60)}"
        
        embed = ds.Embed(color=0xffd8ee,title=f"🌙 `{minute2time(waketime)}`에 일어날 `수면 시간` 추천!",description='-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        embed.add_field(name="4시간 30분 수면",value=f"> ```{minute2time(sleeptime[0])}```\n")
        embed.add_field(name="6시간 00분 수면",value=f"> ```{minute2time(sleeptime[1])}```\n")
        embed.add_field(name="",value="")
        embed.add_field(name="7시간 30분 수면",value=f"> ```{minute2time(sleeptime[2])}```\n")
        embed.add_field(name="9시간 00분 수면",value=f"> ```{minute2time(sleeptime[3])}```\n")
        embed.add_field(name="",value="")
        await interaction.response.send_message(embed=embed)