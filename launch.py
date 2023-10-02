#import
import discord as ds
from discord import app_commands
from discord.ext import commands, tasks

import os
import json

from cogs import append_cogs as ac

#토큰
with open('key.json') as file:
    apiKeys = json.load(file)
    TOKEN = apiKeys["discord"]["bot"]["token"]

#봇 추가
command_prefix = "~"
intents = ds.Intents.all()
bot = commands.Bot(command_prefix=command_prefix,intents=intents)


@bot.event
async def on_ready():
    #준비 완료 알림
    print(f'봇이 준비 되었습니다!\n이름: `{bot.user.name}`\n준비된 서버: `{len(bot.guilds)}개`\n')
    
    #cog 추가
    await ac.add_all(bot)
    
    #슬래시 커맨드 싱크
    print('명령어를 싱크하는 중...')
    await bot.tree.sync(guild=ds.Object(id=1139096712221294612))
    print('완료!')
    
    #상태 변경
    await bot.change_presence(activity=ds.Activity(name='=͟͟͞͞ ͟͟͞͞𖤐 아르는 `~help`를',type=ds.ActivityType.listening))

@bot.tree.command(name="싱크")
async def sync_guild(interaction:ds.Interaction):
    try:
        syncs = await bot.tree.sync(guild=ds.Object(id=interaction.guild.id))
    except Exception as e:
        print(e)
        await interaction.response.send_message("^^^^^\n싱크에 실패했어.. TㅅT")
    else:
        await interaction.response.send_message("싱크에 성공했어! 싱크된 명령어 : `{commands}개`".format(commands=len(syncs)))

#실행
bot.run(TOKEN)