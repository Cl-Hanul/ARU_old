#import
import discord as ds
from discord import app_commands
from discord.ext import commands, tasks

import json

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
    
    #슬래시 커맨드 싱크
    print('명령어를 싱크하는 중...')
    # await bot.tree.sync()
    print('완료!')

@bot.tree.command(name="아니왜슬래시커맨드몇개는되고몇개는안되는데엑",description="``")
async def a(i):
    await i.response.send_message("a")
bot.run(TOKEN)