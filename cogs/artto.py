import discord as ds
from discord import app_commands
from discord.ext import commands, tasks

import json
from datetime import datetime
import asyncio
import aiohttp
from random import randint

from bs4 import BeautifulSoup as BS

# def tellnumber()
async def getball(drw_round:int=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://dhlottery.co.kr/gameResult.do?method=byWin{f'&drwNo={drw_round}' if drw_round else ''}") as response:
            html = await response.text()
    soup = BS(html,"html.parser")
    return [str(ball.get_text()) for ball in soup.find_all("span",{"class":f"ball_645"})]

class ArttoCog(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
        
        self.loadnumber.start()

    @tasks.loop(seconds=10)
    async def loadnumber(self):
        with open('data\\artto.json',"r") as file:
            arttodata = json.load(file)
        if not (datetime.today() - datetime(arttodata['last_date']['year'],arttodata['last_date']['month'],arttodata['last_date']['day'],22,0,0)).days > 6:
            return
        
        balls = await getball()
        
        arttodata['now_round'] += 1
        arttodata['last_date'] = {"year": datetime.now().year, "month": datetime.now().month, "day": datetime.now().day-((datetime.now().weekday() + 2) - (7 if datetime.now().weekday() in [5,6] else 0))}
        arttodata['win_number'][str(arttodata['now_round'])] = balls
        
        with open('data\\artto.json','w') as file:
            json.dump(arttodata,file)
        
        embed = ds.Embed(color=0xffd8ee,title=f"알또 제 {arttodata['now_round']}회 당첨번호!",description="당첨되었는지 확인해보세요!")
        embed.add_field(name=' '.join(balls),value='')
        for channelid in arttodata['tell_channel']:
            channel = self.bot.get_channel(channelid)
            await channel.send(embed=embed)


    @app_commands.command(name="알또구매",description="알또를 구매합니다 (아르코인 10/한 줄)")
    @app_commands.describe(
        line1="띄어쓰기로 구분합니다",
        line2="띄어쓰기로 구분합니다",
        line3="띄어쓰기로 구분합니다",
        line4="띄어쓰기로 구분합니다",
        line5="띄어쓰기로 구분합니다"
    )
    async def buyartto(self,interaction:ds.Interaction,line1:str=None,line2:str=None,line3:str=None,line4:str=None,line5:str=None):
        if (datetime.now().weekday() == 5) & (datetime.now().hour in [8,9]):
            embed = ds.Embed(title="알또 구매 기간이 아닙니다",description="매주 토요일 20:00~21:59에는 구매불가",color=0xffaa66)
            await interaction.response.send_message(embed=embed)
            return
        
        def get_number(var:str):
            if (var == None):
                return None
            test1 = False if (len(var.split(' ')) != 6) else True
            for i in var.split(' '):
                try:
                    int(i)
                except:
                    test2 = False
                    break
                if (int(i) < 1) or (int(i) > 45):
                    test2 = False
                    break
                test2 = True
            
            return var.split(' ') if test1 & test2 else None
        
        with open('data\\artto.json',"r") as file:
            arttodata = json.load(file)
            if interaction.user.id not in arttodata['userdata']:
                arttodata['userdata'][str(interaction.user.id)] = {"artto":[]}
        userartto = arttodata['userdata'][str(interaction.user.id)]
        artto = {'number':[],"round":arttodata['now_round']}
        for line in [line1,line2,line3,line4,line5]:
            if line == 'j':
                linetest = ['Jadong']+[randint(1,45) for i in range(6)]
            elif get_number(line):
                linetest = ['Sudong']+get_number(line)    
            else:
                continue
            artto['number'].append(linetest)
        userartto['artto'].append(artto)
        
        embed = ds.Embed(title="알또로또 제 n회",description="결과발표일 ****년 **월 **일 ",color=0xffd8ee)
        for line in artto['number']:
            if line != None:
                print(artto['number'])
                embed.add_field(name=f"{'자동 | ' if line[0] == 'Jadong' else '수동 | '}{' '.join(map(str,line[1:]))}",value="",inline=False)
        
        if len(embed.fields) == 0:
            del userartto['artto'][-1]
        with open('data\\artto.json',"w") as file:
            json.dump(arttodata,file)
        
        if len(embed.fields) == 0:
            embed = ds.Embed(title="입력된 번호가 없어 구입처리가 취소되었습니다",description="번호는 띄어쓰기로 구분했는지, 범위 안에 입력했는지, 숫자 갯수가 5개인지 확인해줘!",color=0xffaa66)
            await interaction.response.send_message(embed=embed)
            return
        await interaction.response.send_message("# `알또` 구매가 완료되었습니다.\n아르 코인 -30",embed=embed)

    @app_commands.command(name="알또알림",description="알또의 새로운 번호 알림을 받을 채널을 선택합니다.")
    async def setarttotell(self,interaction:ds.Interaction,tellchannel:ds.TextChannel):
        with open('data\\artto.json',"r") as file:
            arttodata = json.load(file)
        if tellchannel.id not in arttodata['tell_channel']:
            arttodata['tell_channel'].append(tellchannel.id)
            await interaction.response.send_message(f"<#{tellchannel.id}>를 알또 알림채널로 설정합니다~!")
        else:
            arttodata['tell_channel'].remove(tellchannel.id)
            await interaction.response.send_message(f"<#{tellchannel.id}>의 알또 알림채널을 설정해제했습니다~!")
        with open('data\\artto.json','w') as file:
            json.dump(arttodata,file)
    
    @app_commands.command(name='알또당첨확인',description="구매한 알또의 당첨 여부를 확인할 수 있어요!")
    @app_commands.describe(
        rounds="알또의 회차 수"
    )
    async def checkartto(self,interaction:ds.Interaction,rounds:str):
        with open('data\\artto.json','r') as file:
            arttodata = json.load(file)
        if rounds not in arttodata['win_number']:
            await interaction.response.send_message("회차 데이터가 존재하지 않아!")
            return
        embed = ds.Embed(color=0xffd8ee,title=f"알또 제 {rounds}회 당첨번호!",description="")
        embed.add_field(name=f"당첨번호",value="보너스")
        embed.add_field(name=f" | ",value=" | ")
        embed.add_field(name=f"{' '.join(map(str,arttodata['win_number'][rounds][:-2]))}",
                        value=f"{arttodata['win_number'][rounds][-1]}")
        await interaction.response.send_message(embed=embed)