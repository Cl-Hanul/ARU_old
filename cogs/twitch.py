import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import *

from API.twitch_API import get_stream,get_user

def getStreamLogin(StreamLinkOrLogin:str) -> str:
    if "twitch.tv/" in StreamLinkOrLogin:
        StreamLogin = StreamLinkOrLogin[StreamLinkOrLogin.find('twitch.tv/')+10:]
        if '/' in StreamLogin:
            StreamLogin = StreamLogin[:StreamLogin.find('/')]
        return StreamLogin
    else:
        return StreamLinkOrLogin

    
class Twitch(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.InformList = {}
    
    @app_commands.command(name="streaminfo",description="show stream infomation.")
    async def streaminfo(self,interaction:ds.Interaction,streamlinkorlogin:str):
        StreamLogin = getStreamLogin(streamlinkorlogin)
        
        try:
            StreamingData = get_stream(StreamLogin)
        except:
            embed = ds.Embed(color=0xff7777,title='아르가 방송 정보를 불러오지 못했어.. ㅜ-ㅜ',description='입력한 `링크`나 `로그인`을 다시 확인해줘!')
            embed.set_thumbnail(url="https://static-cdn.jtvnw.net/ttv-static/404_preview-128x128.jpg")
        else:
            if StreamingData.stream == True:
                embed = ds.Embed(color=0x77ff77,url=f"https://www.twitch.tv/{StreamLogin}")
                if StreamingData.user_login == StreamingData.user_name:
                    embed.title = f"'`{StreamingData.user_login}`'님은 지금 방송하고 있어!! ≧▽≦"
                else:
                    embed.title = f"'`{StreamingData.user_name}({StreamingData.user_login})`'님은 지금 방송하고 있어!! ≧▽≦"
                embed.add_field(name=StreamingData.title,value=StreamingData.category)
                embed.set_thumbnail(url=get_user(StreamingData.user_login).profile_image_url)      
                embed.set_image(url=StreamingData.thumbnail_url.format(width=1080,height=640))
            else:
                userData = get_user(StreamLogin)
                if userData.exist:
                    embed = ds.Embed(color=0x7777ff,url=f"https://www.twitch.tv/{StreamLogin}")
                    if userData.login == userData.display_name:
                        embed.title = f"'`{userData.login}`'님은 아직 방송 준비 중이야! QvQ"
                    else:
                        embed.title = f"'`{userData.display_name}({userData.login})`'님은 아직 방송 준비 중이야! QvQ"
                    embed.description = userData.description
                    embed.set_thumbnail(url=userData.profile_image_url)
                    embed.set_image(url=userData.offline_image_url)
        await interaction.response.send_message(embed=embed)        