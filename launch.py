#import
import discord as ds
from discord.ext import commands

import os
import json

from cogs import append_cogs as ac

#토큰
with open('key.json') as file:
    TOKEN = json.load(file)["discord"]["bot"]["token"]

#봇 추가
command_prefix = "~"
intents = ds.Intents.all()
bot = commands.Bot(command_prefix=command_prefix,intents=intents)

@bot.event
async def on_ready():
    #준비 완료 알림
    print('your bot is ready!')
    
    #cog 추가
    await ac.add_all(bot)
    
    #슬래시 커맨드 싱크
    await bot.tree.sync()
    
    #상태 변경
    await bot.change_presence(activity=ds.Activity(name='아르는 `~help`를',type=ds.ActivityType.listening))    

@bot.tree.command(name="싱크")
async def sync_guild(interaction:ds.Interaction):
    try:
        bot.tree.sync(guild=bot.get_guild(interaction.guild.id))
        await interaction.response.send_message("싱크에 성공했어!")
    except:
        await interaction.response.send_message("싱크에 실패했어.. TㅅT")
        

#실행
bot.run(TOKEN)

os.system("pause")