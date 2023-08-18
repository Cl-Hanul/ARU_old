import discord as ds
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import View, Button

import json

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
    def __init__(self,bot:commands.Bot) -> None:
        #변수 작성
        self.bot = bot
        self.Informed = {}

        #루프 실행
        self.streamInform.start()
    
    #알림 기능
    @tasks.loop(seconds=60)
    async def streamInform(self):
        #리스트 불러오기
        with open('data\\twitch.json') as file:
            InfromList = json.load(file)
        #스트리머 만큼 반복
        for StreamLogin in InfromList.keys():
            #스트리머가 이미 알림 변수에 없을 때
            if StreamLogin not in self.Informed:
                self.Informed[StreamLogin] = []
            
            try:
                StreamData = get_stream(StreamLogin)
            except:
                pass #스트리머가 없어지거나, 스트리머를 찾을 수 없을 때
                return
            if StreamData.stream:               
                #임베드 생성 및 전송
                for ChannelId in InfromList[StreamLogin]:
                    print(ChannelId)
                    InformChannel = self.bot.get_channel(ChannelId)
                    
                    if ChannelId not in self.Informed[StreamLogin]:
                        self.Informed[StreamLogin].append(ChannelId)
                        embed = ds.Embed(color=0x77ff77,url=f"https://www.twitch.tv/{StreamLogin}")
                        if StreamData.user_login == StreamData.user_name:
                            embed.title = f"'`{StreamData.user_login}`'님이 방송하는 중!!"
                        else:
                            embed.title = f"'`{StreamData.user_name}({StreamData.user_login})`'님이 방송하는 중!!"
                        embed.add_field(name=StreamData.title,value=StreamData.category)
                        embed.set_thumbnail(url=get_user(StreamData.user_login).profile_image_url)
                        embed.set_image(url=StreamData.thumbnail_url.format(width=1080,height=640))
                        await InformChannel.send(embed=embed)
                        

                    
        
            
    @app_commands.command(name="방송정보",description="아르가 스트리머의 정보를 가져와줘!")
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
        ##콜백
        async def add_stream(interaction:ds.Interaction):
            ###파일불러오기
            with open('data\\twitch.json',"r") as file:
                InformList = json.load(file)
            ###파일에 스트리머 등록 여부
            if str(StreamLogin) not in InformList:
                InformList[str(StreamLogin)] = []
            ###해당 채널 등록 여부
            if interaction.channel.id not in InformList[str(StreamLogin)]:
                InformList[str(StreamLogin)].append(interaction.channel.id)
                embed = ds.Embed(color=0xffff00,title="이제부터 스트리머가 방송을 킬 때마다 아르가 여기에 알려줄게!")
            else:
                embed = ds.Embed(color=0xffaa00,title="이미 아르는 여기에 알리고 있어!")
            with open('data\\twitch.json',"w") as file:
                json.dump(InformList,file)
            await interaction.response.send_message(embed=embed)
        button = Button(style=ds.ButtonStyle.primary,label="🔔")
        button.callback = add_stream
        view = View(timeout=15)    
        view.add_item(button)

        #embed 및 view 전송
        await interaction.response.send_message(embed=embed,view=view)