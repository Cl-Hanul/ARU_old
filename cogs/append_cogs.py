import discord as ds
from discord.ext import commands

from cogs.twitch import Twitch
from cogs.item import ItemCog
from cogs.welcome import Welcome
from cogs.neis import Neis

async def add_all(bot:commands.Bot):
    cogs = [
        {"name":"twitch","cog":Twitch(bot)},
        {"name":"item","cog":ItemCog(bot)},
        {"name":"Welcome","cog":Welcome(bot)},
        {"name":"Neis","cog":Neis(bot)}
    ]
    
    for i in cogs:
        try:
            await bot.add_cog(i["cog"])
            print(f"'{i['name']}'cog를 불러오는 중...")
        except Exception as e:
            print("불러오기 실패\n\n" + e)
        else:
            print("불러오기 성공!")