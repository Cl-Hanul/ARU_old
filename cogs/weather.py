import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Select, Button

import json

class Weather(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="위치설정",description="아르가 날씨를 알려줄 때 참고할 정보")
    @app_commands.describe(rlg="광역자치단체(Regional Local Government)")
    @app_commands.choices(rlg=[
        app_commands.Choice(name="서울특별시",value="서울특별시"),
        app_commands.Choice(name="부산광역시",value="부산광역시"),
        app_commands.Choice(name="대구광역시",value="대구광역시"),
        app_commands.Choice(name="인천광역시",value="인천광역시"),
        app_commands.Choice(name="광주광역시",value="광주광역시"),
        app_commands.Choice(name="대전광역시",value="대전광역시"),
        app_commands.Choice(name="울산광역시",value="울산광역시"),
        app_commands.Choice(name="세종특별자치시",value="세종특별자치시"),
        app_commands.Choice(name="경기도",value="경기도"),
        app_commands.Choice(name="충청북도",value="충청북도"),
        app_commands.Choice(name="충청남도",value="충청남도"),
        app_commands.Choice(name="전라북도",value="전라북도"),
        app_commands.Choice(name="전라남도",value="전라남도"),
        app_commands.Choice(name="경상북도",value="경상북도"),
        app_commands.Choice(name="경상남도",value="경상남도"),
        app_commands.Choice(name="제주특별자치도",value="제주특별자치도"),
        app_commands.Choice(name="이어도",value="이어도"),
        app_commands.Choice(name="강원특별자치도",value="강원특별자치도")
    ])
    async def setposition(self, interaction:ds.Interaction, rlg:app_commands.Choice[str]):
        with open('info\\kor_position.json','r') as file:
            kor_position = json.load(file)
        show_position = kor_position[rlg.value]
        
        res = False
        page = 0
        pageend = len(show_position)%10 +1
        def embed() -> ds.Embed:
            embed = ds.Embed(title="지역을 선택해주세요",description="날씨정보를 알아볼 수 있습니다")
            return embed
        async def makeview(res,interaction:ds.Interaction,number, page):
            page += number
            view = View()
            rev = Button(label="⬅️",disabled=True if page == 0 else False)
            nev = Button(label="➡️",disabled=True if page == pageend else False)
            
            async def rev_callback(interaction:ds.Interaction):
                view = await makeview(res,interaction,-1,page)
            rev.callback = rev_callback
            async def nev_callback(interaction:ds.Interaction):
                view = await makeview(res,interaction,1,page)
            nev.callback = nev_callback
            view.add_item(rev)
            view.add_item(nev)
            if not res:
                await interaction.response.send_message(page,view=view)
                res = True
            else:
                await interaction.response.edit_message(content=page,view=view)
        await makeview(res,interaction, 0, page)