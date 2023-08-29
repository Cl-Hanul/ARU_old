import discord as ds
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import View, Select

import json
from datetime import datetime

from API.neis_API import get_meal, get_school_by_name

class Neis(commands.Cog):
    meal = app_commands.Group(name="급식",description="급식 설명")
    
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
        
        self.meal_alert.start()
    
    @tasks.loop(seconds=60)
    async def meal_alert(self):
        now = datetime.strftime(datetime.now(),"%H%M")
        today = datetime.strftime(datetime.now(),"%Y%m%d")
        with open('data\\neis.json') as file:
            mealList = json.load(file)["meal"]
        
        for fdcdcschool in mealList:
            mealData = get_meal(fdcdcschool[:3],fdcdcschool[3:],today)
            if not mealData.body:
                continue
            for time in mealList[fdcdcschool]:
                if time != now:
                    continue
                for inform in mealList[fdcdcschool][time]:
                    embed = ds.Embed(color=0xffd8ee,title="❗급식이 떳다!",description=f"'`{mealData.body[int(inform['mealId'])-1].school_name}`' 오늘의 급식 알림!")
                    embed.add_field(name=mealData.body[inform['mealId']-1].meal_name.replace('조식','⛅조식').replace('중식','☀️중식').replace('석식','🌙석식'),value=f"> "+mealData.body[inform['mealId']-1].dishes.replace('\n','\n> ')+"\n```"+'\n'.join(mealData.body[inform['mealId']-1].ntr[:3])+"```")
                    try:
                        await self.bot.get_channel(inform["channelId"]).send(embed=embed)
                    except Exception as e:
                        print(e)

    @meal.command(name="학교설정",description="급식 명령어 이용을 위해 학교 정보를 입력합니다.")
    @app_commands.describe()
    async def meal_setting_school(self,interaction:ds.Interaction,school_name:str):
        schoolData = get_school_by_name(school_name)
        if not schoolData:
            await interaction.response.send_message("학교 못찾음")
            return
        
        view = View()
        selection = Select(options=[ds.SelectOption(label=school["name"],value=f'{school["ofcdc_code"]}{school["code"]}',description=school["pos"]) for school in schoolData])
        schoolnames = {}
        for schoolSelectOption in selection.options:
            schoolnames[schoolSelectOption.value] = schoolSelectOption.label
            
        async def selection_callback(interaction:ds.Interaction):
            with open('data\\neis.json') as file:
                userSchool = json.load(file)
            if str(interaction.user.id) not in userSchool["school"]:
                userSchool["school"][str(interaction.user.id)] = selection.values[0]
                await interaction.response.send_message(f"`{schoolnames[selection.values[0]]}`로 학교 설정을 이전합니다.",ephemeral=True)
                if selection.values not in userSchool["meal"]:
                    userSchool["meal"][selection.values] = {}
            elif str(interaction.user.id) == userSchool["school"][str(interaction.user.id)]:
                await interaction.response.send_message("이미 그 학교로 설정되있음.")
            else:
                userSchool["school"][str(interaction.user.id)] = selection.values[0]
                await interaction.response.send_message(f"이제부터 설정된 학교는 `{schoolnames[selection.values[0]]}` 입니다.",ephemeral=True)
                if selection.values not in userSchool["meal"]:
                    userSchool["meal"][selection.values] = {}
            with open('data\\neis.json',"w") as file:
                json.dump(userSchool,file)
        selection.callback = selection_callback
        view.add_item(selection)
        await interaction.response.send_message(view=view,ephemeral=True)
    
    @meal.command(name="알림추가",description="매주 설정 시간에 급식 알림을 이 채널에 추가합니다.")
    @app_commands.describe(alert_time="24시간 형식의 '시시분분' 형식으로 입력합니다. 예)2104")
    @app_commands.describe(meal_id="알림 받을 급식을 정합니다(조식,중식,석식)")
    @app_commands.choices(meal_id=[
        app_commands.Choice(name="조식", value="1"),
        app_commands.Choice(name="중식", value="2"),
        app_commands.Choice(name="석식", value="3"),
    ])
    async def add_meal_alert(self,interaction:ds.Interaction,alert_time:str,meal_id:app_commands.Choice[str]):
        with open('data\\neis.json') as file:
            neisData = json.load(file)
        if str(interaction.user.id) not in neisData["school"]:
            await interaction.response.send_message("`/급식 학교설정` 명령어를 먼저 이용해 주세요")
            return
        code_all = neisData["school"][str(interaction.user.id)]
        if alert_time not in neisData["meal"][code_all]:
            neisData["meal"][code_all][alert_time] = []
        neisData["meal"][code_all][alert_time].append({"channelId": interaction.channel.id, "mealId": meal_id.value})
        with open('data\\neis.json',"w") as file:
            json.dump(neisData,file)
        await interaction.response.send_message(f"이제부터 매 주 '`{alert_time[:2]}시 {alert_time[2:]}분`'에 '`{meal_id.name}`'을 이 채널로 알려줍니다.")
        

    
    
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
            embed.add_field(name=f"{m.meal_name.replace('조식','⛅조식').replace('중식','☀️중식').replace('석식','🌙석식')} ({m.calories})",value=f"> "+m.dishes.replace('\n','\n> ')+"\n```"+'\n'.join(m.ntr[:3])+"```")
        
        await interaction.response.send_message(embed=embed)
        
        