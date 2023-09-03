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
                    embed = ds.Embed(color=0xffd8ee,title="❗아르가 알려주는 `오늘의 메뉴`!",description=f"'`{mealData.body[int(inform['mealId'])-1].school_name}`' 오늘의 급식 알림!")
                    embed.add_field(name=mealData.body[inform['mealId']-1].meal_name.replace('조식','⛅아침밥').replace('중식','☀️점심밥').replace('석식','🌙저녁밥'),value=f"> "+mealData.body[inform['mealId']-1].dishes.replace('\n','\n> ')+"\n```"+'\n'.join(mealData.body[inform['mealId']-1].ntr[:3])+"```")
                    try:
                        await self.bot.get_channel(inform["channelId"]).send(embed=embed)
                    except Exception as e:
                        print(e)

    @meal.command(name="학교설정",description="아르가 학교를 참고할 수 있게 해주는 명령어!")
    @app_commands.describe()
    async def meal_setting_school(self,interaction:ds.Interaction,school_name:str):
        if len(school_name) < 2:
            embed = ds.Embed(color=0xffaa66,title="학교 이름은 2글자 이상으로 입력해줘!",description="정확히 입력해줘야 돼!")
            await interaction.response.send_message(embed=embed)
            return
        if len(school_name) > 24:
            embed = ds.Embed(color=0xffaa66,title="학교 이름은 24글자 이하로 입력해줘!",description="정확히 입력해줘야 돼!")
            await interaction.response.send_message(embed=embed)
            return
        schoolData = get_school_by_name(school_name)
        if not schoolData:
            embed = ds.Embed(color=0xee6666,title="어.. 아르가 찾아 봤는데, 그런 학교는 없는 것 같아!",description="띄어쓰기나 철자를 다시 확인해줘!")
            await interaction.response.send_message(embed=embed)
            return

        view = View()
        selection = Select(placeholder="아르가 열심히 찾아왔으니 선택해줘!", options=[ds.SelectOption(label=school["name"],value=f'{school["ofcdc_code"]}{school["code"]}',description=school["pos"]) for school in schoolData])
        schoolnames = {}
        for schoolSelectOption in selection.options:
            schoolnames[schoolSelectOption.value] = schoolSelectOption.label
            
        async def selection_callback(interaction:ds.Interaction):
            with open('data\\neis.json') as file:
                userSchool = json.load(file)
            if str(interaction.user.id) in userSchool["school"]:
                userSchool["school"][str(interaction.user.id)] = selection.values[0]
                embed = ds.Embed(color=0xffd8ee,title=f"사실 `{schoolnames[selection.values[0]]}` 였구나!",description="이제 아르는 그렇게 알고 있을게!")
                await interaction.response.send_message(embed=embed,ephemeral=True)
                if selection.values[0] not in userSchool["meal"]:
                    userSchool["meal"][selection.values] = {}
            elif selection.values[0] == userSchool["school"][str(interaction.user.id)]:
                embed = ds.Embed(color=0x66ff66,title="아르한테 이미 그 학교로 알려줬어!",description="적용은 잘 되있어!")
                await interaction.response.send_message(embed=embed,ephemeral=True)
            else:
                userSchool["school"][str(interaction.user.id)] = selection.values[0]
                embed = ds.Embed(color=0xffd8ee,title="알려줘서 고마워!",description=f"아르는 이제 `{schoolnames[selection.values[0]]}`로 알고 있을게!")
                await interaction.response.send_message(embed=embed,ephemeral=True)
                if selection.values[0] not in userSchool["meal"]:
                    userSchool["meal"][selection.values[0]] = {}
            with open('data\\neis.json',"w") as file:
                json.dump(userSchool,file)
        selection.callback = selection_callback
        view.add_item(selection)
        await interaction.response.send_message(view=view,ephemeral=True)
    
    @meal.command(name="알림추가",description="아르가 그 날에 급식을 알려줘!")
    @app_commands.describe(alert_time="24시간 형식의 '시시분분' 예)2104")
    @app_commands.describe(meal_id="알림 받을 급식 (아침,점심,저녁)")
    @app_commands.choices(meal_id=[
        app_commands.Choice(name="아침", value="1"),
        app_commands.Choice(name="점심", value="2"),
        app_commands.Choice(name="저녁", value="3"),
    ])
    async def add_meal_alert(self,interaction:ds.Interaction,alert_time:str,meal_id:app_commands.Choice[str]):
        if int(alert_time[:2]) == 24:
            alert_time = "00" + alert_time[2:4]
        if int(alert_time[:2]) < 0 | int(alert_time[2:4]) > 59 | int(alert_time[2:4]) < 0:
            embed = ds.Embed(color=0xffaa66,title="존재하는 시간으로 입력해줘!",description="아르의 시계는 23시랑 59분을 넘어가는 시계가 없어!")
            await interaction.response.send_message(embed=embed)
            return
        with open('data\\neis.json') as file:
            neisData = json.load(file)
        if str(interaction.user.id) not in neisData["school"]:
            embed = ds.Embed(color=0xffaa66,title="`/급식 학교설정`로 아르한테 학교를 먼저 알려줘!",description="그래야 아르가 급식을 알려줄 수 있어!")
            await interaction.response.send_message(embed=embed)
            return
        code_all = neisData["school"][str(interaction.user.id)]
        if alert_time not in neisData["meal"][code_all]:
            neisData["meal"][code_all][alert_time] = []
        neisData["meal"][code_all][alert_time].append({"channelId": interaction.channel.id, "mealId": meal_id.value})
        with open('data\\neis.json',"w") as file:
            json.dump(neisData,file)
        embed = ds.Embed(color=0xffd8ee,title=f"'`{alert_time[:2]}시 {alert_time[2:]}분`'에 '`{meal_id.name}`' 접수완료~!",description=f"이제부터 아르가 매 주 `{meal_id.name}`을 알려줄게!")
        await interaction.response.send_message(embed=embed)
        

    
    
    @meal.command(name="정보",description="아르가 학교의 급식을 알려줘!")
    @app_commands.describe(school_name="학교 이름! 예)'00중학교'")
    @app_commands.describe(meal_date="급식 날짜! 예)20230124")
    async def meal_info(self,interaction:ds.Interaction,school_name:str,meal_date:int):
        school = get_school_by_name(school_name)
        
        if not school:
            embed = ds.Embed(color=0xee6666,title="어.. 아르가 찾아 봤는데, 그런 학교는 없는 것 같아!",description="띄어쓰기나 철자를 다시 확인해줘!")
            await interaction.response.send_message(embed=embed)
            return
        
        meal = get_meal(school[0]['ofcdc_code'],school[0]['code'],meal_date)
        if not meal.body:
            embed = ds.Embed(color=0xff48ee,title="급식이 없어..",description="큰일이야..!!")
            await interaction.response.send_message(embed=embed)
            return
        
        embed = ds.Embed(color=0xffd8ee, title=f"{meal.body[0].school_name}",description=f"아르가 알려주는 **'{str(meal_date)[:4]}년 {str(meal_date)[4:6]}월 {str(meal_date)[6:]}일'** 급식!")
        embed.add_field(name="---",value="",inline=False)
        for m in meal.body:
            embed.add_field(name=f"{m.meal_name.replace('조식','⛅아침밥').replace('중식','☀️점심밥').replace('석식','🌙저녁밥')} ({m.calories})",value=f"> "+m.dishes.replace('\n','\n> ')+"\n```"+'\n'.join(m.ntr[:3])+"```")
        
        await interaction.response.send_message(embed=embed)