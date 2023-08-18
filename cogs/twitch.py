import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

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
    def __init__(self,bot,InformList) -> None:
        self.bot = bot
        self.InformList = InformList
        self.Informed = {}
    
    @app_commands.command(name="streaminfo",description="show stream infomation.")
    async def streaminfo(self,interaction:ds.Interaction,streamlinkorlogin:str):
        #스트리밍 로그인 가져오기
        StreamLogin = getStreamLogin(streamlinkorlogin)
        
        try:
            #스트리밍 데이터 가져오기
            StreamingData = get_stream(StreamLogin)
        except:
            #만일 스트리밍의 데이터를 가져오지 못한 경우
            embed = ds.Embed(color=0xff7777,title='아르가 방송 정보를 불러오지 못했어.. ㅜ-ㅜ',description='입력한 `링크`나 `로그인`을 다시 확인해줘!')
            embed.set_thumbnail(url="https://static-cdn.jtvnw.net/ttv-static/404_preview-128x128.jpg")
        else:
            if StreamingData.stream == True:
                #스트리머가 현재 스트리밍 중일 때
                embed = ds.Embed(color=0x77ff77,url=f"https://www.twitch.tv/{StreamLogin}")
                if StreamingData.user_login == StreamingData.user_name:
                    embed.title = f"'`{StreamingData.user_login}`'님은 지금 방송하고 있어!! ≧▽≦"
                else:
                    embed.title = f"'`{StreamingData.user_name}({StreamingData.user_login})`'님은 지금 방송하고 있어!! ≧▽≦"
                embed.add_field(name=StreamingData.title,value=StreamingData.category)
                embed.set_thumbnail(url=get_user(StreamingData.user_login).profile_image_url)      
                embed.set_image(url=StreamingData.thumbnail_url.format(width=1080,height=640))
            else:
                #스트리머가 현재 오프라인 일 때
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
        
        #버튼 및 view 추가
        async def add_stream(interaction:ds.Interaction):
            if str(StreamLogin) not in self.InformList:
                self.InformList
            await interaction.response.send_message("is clicked!")
        button = Button(style=ds.ButtonStyle.primary,label="🔔")
        button.callback = add_stream
        view = View(timeout=15)    
        view.add_item(button)

        #embed 및 view 전송
        await interaction.response.send_message(embed=embed,view=view)