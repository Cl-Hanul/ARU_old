import discord as ds
from discord.ext import commands

from cogs.twitch import Twitch
from cogs.item import ItemCog
from cogs.welcome import Welcome
from cogs.neis import Neis
from cogs.other import Other
from cogs.custom_embed import CustomEmbed
from cogs.weather import Weather
from cogs.music import Music

async def add_all(bot:commands.Bot):
    cogs = [Twitch,ItemCog,Welcome,Neis,Other,CustomEmbed,Weather,Music]
    
    for i in cogs:
        try:
            await bot.add_cog(i(bot))
            print(f"'{i.__name__}'cog를 불러오는 중...")
        except Exception as e:
            print("불러오기 실패\n\n" + str(e))
        else:
            print("불러오기 성공!")