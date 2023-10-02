import discord as ds
from discord import app_commands
from discord.ext import commands

from API.kor_law_API import SearchLaw

class Law(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="법령검색",description="대한민국의 법령을 검색합니다")
    @app_commands.choices(searchtype=[
        app_commands.Choice(name="법령 제목으로 검색", value=1),
        app_commands.Choice(name="법령 본문으로 검색", value=2)
    ])
    @app_commands.describe(
        query="법령을 검색할 내용입니다",
        searchtype="법령을 검색할 방법입니다"
    )
    async def searchlaw(self,interaction:ds.Interaction,searchtype:app_commands.Choice[int],query:str):
        lawdata = SearchLaw(searchtype.value,query)
        if not lawdata:
            await interaction.response.send_message("검색결과가 없습니다")
            return
        embed = ds.Embed(color=0xffd8ee,title="법령검색",description=f"`{query}`에 대한 법령 검색 결과입니다")
        embed.url = f"https://law.go.kr/LSW/lsSc.do?menuId=1&subMenuId=15&tabMenuId={81 if searchtype.value==1 else 83}&query={query}"
        for i in lawdata:
            embed.add_field(name="a",value="a")
            print(i)
        await interaction.response.send_message(embed=embed)