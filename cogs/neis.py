import discord as ds
from discord import app_commands
from discord.ext import commands

from API.neis_API import get_meal, get_school_by_name

class Neis(commands.Cog):
    meal = app_commands.Group(name="급식",description="급식 설명")
    
    def __init__(self,bot) -> None:
        self.bot = bot
        
    @meal.command(name="정보",description="학교의 급식을 알려줍니다.")
    @app_commands.describe(school_name="학교 이름 예)'00중학교'")
    @app_commands.describe(meal_date="급식 날짜 예)20230124")
    async def meal_info(self,interaction:ds.Interaction,school_name:str,meal_date:int):
        school = get_school_by_name(school_name)
        
        if not school:
            await interaction.response.send_message("학교 못찾음")
            return
        
        meal = get_meal(school[0]['ofcdc_code'],school[0]['code'],meal_date)
        if not meal.body:
            await interaction.response.send_message("급식 없음")
            return
        
        embed = ds.Embed(color=0xffd8ee, title=f"{meal.body[0].school_name}",description=f"**'{str(meal_date)[:4]}년 {str(meal_date)[4:6]}월 {str(meal_date)[6:]}일'** 급식!")
        embed.add_field(name="---",value="",inline=False)
        for m in meal.body:
            embed.add_field(name=f"{m.meal_name.replace('조식','⛅조식').replace('☀️중식','중식').replace('🌙석식','석식')} ({m.calories})",value=f"> "+m.dishes.replace('\n','\n> ')+"\n```"+'\n'.join(m.ntr[:3])+"```")
        
        await interaction.response.send_message(embed=embed)
        
        