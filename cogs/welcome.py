import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button

import json

class Welcome(commands.Cog):
    Visit = app_commands.Group(name="방문알림",description="방문알림과 관련된 명령어")
    
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member:ds.Member):
        with open("data\\visit.json") as file:
            visitData = json.load(file)
        
        if str(member.guild.id) not in visitData:
            return
        if self.bot.get_channel(visitData[str(member.guild.id)]["in"]) == None:
            return
        await self.bot.get_channel(visitData[str(member.guild.id)]["in"]).send(member.mention + "짱!\n한울 서버에 온걸 환영해! ><")
    
    @commands.Cog.listener()
    async def on_member_remove(self,member:ds.Member):
        with open("data\\visit.json") as file:
            visitData = json.load(file)
        
        if str(member.guild.id) not in visitData:
            return
        if self.bot.get_channel(visitData[str(member.guild.id)]["out"]) == None:
            return
        await self.bot.get_channel(visitData[str(member.guild.id)]["out"]).send(member.mention + "짱ㅜㅜ\n떠나도.. 한울 서버는 잊지 말아줘 T^T")
    
    @Visit.command(name="설정")
    async def streamInform(self,interaction:ds.Interaction):
        with open("data\\visit.json") as file:
            visitData = json.load(file)
        if interaction.guild.id not in visitData:
            visitData[interaction.guild.id] = {"in":0,"out":0}
        with open('data\\visit.json',"w") as file:
            json.dump(visitData,file)

        selectIn = Select(options=[ds.SelectOption(label=channel.name,value=str(channel.id),description="Text Channel") for channel in interaction.guild.channels if type(channel) in [ds.channel.TextChannel]],placeholder="입장 알림 채널")
        selectOut = Select(options=[ds.SelectOption(label=channel.name,value=str(channel.id),description="Text Channel") for channel in interaction.guild.channels if type(channel) in [ds.channel.TextChannel]],placeholder="퇴장 알림 채널")
        view = View()
        view.add_item(selectIn)
        view.add_item(selectOut)

        async def selectIncallback(i:ds.Interaction):
            with open("data\\visit.json","r") as file:
                visitData = json.load(file)
            
            visitData[str(i.guild.id)]["in"] = int(selectIn.values[0])
            
            with open("data\\visit.json","w") as file:
                json.dump(visitData,file)
            
            await i.response.edit_message(content=".")
        
        async def selectOutcallback(i:ds.Interaction):
            with open("data\\visit.json","r") as file:
                visitData = json.load(file)
            
            visitData[str(i.guild.id)]["out"] = int(selectOut.values[0])
            
            with open("data\\visit.json","w") as file:
                json.dump(visitData,file)
            
            await i.response.edit_message(content=".")

        selectIn.callback = selectIncallback
        selectOut.callback = selectOutcallback

        await interaction.response.send_message(".",view=view)
        