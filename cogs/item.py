import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button, ChannelSelect

import json
from random import randint

def per(percentage:float):
    if randint(0,10000) <= percentage*100:
        return True
    else:
        return False

def upgradelvl(lvl) -> int | float:
    if per(0.01):
        return None
    if lvl > 200:
        if per(15):
            return int(lvl+randint(5,10))
    elif lvl > 100:
        if per(30):
            return int(lvl+randint(5,10))
    elif lvl > 80:
        if per(55):
            return int(lvl+randint(5,10))
    elif lvl > 50:
        if per(70):
            return int(lvl+randint(5,10))
    elif lvl > 30:
        if per(80):
            return int(lvl+randint(5,10))
    elif lvl > 10:
        if per(90):
            return int(lvl+randint(5,10))
    else:
        return int(lvl+randint(5,10))
    return int(lvl*(randint(50,100)/100))
    
        

class ItemCog(commands.Cog):
    item = app_commands.Group(name="아이템", description="아이템 설명")
    def __init__(self,bot) -> None:
        self.bot = bot
    
    @item.command(name="제작",description="강화할 아이템을 제작할 수 있습니다.")
    @app_commands.describe(itemname="제작될 아이템의 이름입니다 (1~20)")
    @app_commands.describe(itemdescription="제작될 아이템의 설명입니다 (1~100)")
    async def itemmake(self, interaction:ds.Interaction, itemname:str,itemdescription:str):
        if len(itemname) < 1:
            await interaction.response.send_message("아이템의 이름은 최소 1자 이상이어야 합니다")
            return
        elif len(itemname) > 20:
            await interaction.response.send_message("아이템의 이름은 20자를 초과할 수 없습니다")
            return
        elif len(itemdescription) < 1:
            await interaction.response.send_message("아이템의 설명은 최소 1자 이상이어야 합니다")
            return
        elif len(itemdescription) > 100:
            await interaction.response.send_message("아이템의 설명은 100자를 초과할 수 없습니다")
            return
        
        with open('data\\item.json', encoding="UTF8") as file:
            items = json.load(file)
        if str(interaction.user.id) not in items:
            items[str(interaction.user.id)] = []
        
        items[str(interaction.user.id)].append(
            {"name":itemname,
            "lvl":1,
            "description":itemdescription}
        )
        with open('data\\item.json',"w") as file:
            json.dump(items,file)
        embed = ds.Embed(title=f'{itemname} Lv.1',description=itemdescription)
        await interaction.response.send_message("아이템을 제작하였습니다\n제작된 아이템:",embed=embed)
    
    @item.command(name="정보",description="자신이 소지하고 있는 아이템의 정보를 알려줍니다.")
    async def iteminfo(self, interaction:ds.Interaction):
        with open('data\\item.json', encoding="UTF8") as file:
            items = json.load(file)
        
        async def callbacky(interaction:ds.Interaction):
            embed = ds.Embed(title=f'{eval(itemselect.values[0])["name"]} Lv.{eval(itemselect.values[0])["lvl"]}',description=eval(itemselect.values[0])["description"])
            viewe = View()
            upgrade = Button(style=ds.ButtonStyle.green,label="⬆️강화")
            async def itemupgrade(interaction:ds.Interaction):
                with open('data\\item.json',encoding="UTF8") as file:
                    myitems = json.load(file)
                viewe = View()
                itempos = next((index for (index, item) in enumerate(myitems[str(interaction.user.id)]) if item["name"] == eval(itemselect.values[0])["name"]),None)
                if itempos == None:
                    await interaction.message.delete()
                    return
                before = myitems[str(interaction.user.id)][itempos]["lvl"]
                myitems[str(interaction.user.id)][itempos]["lvl"] = upgradelvl(myitems[str(interaction.user.id)][itempos]["lvl"])
                if myitems[str(interaction.user.id)][itempos]["lvl"] == None:
                    content = f"터졌습니다 | 최고 기록:{before}"
                    embed = ds.Embed(color=0xff0000)
                elif myitems[str(interaction.user.id)][itempos]["lvl"] < before:
                    content = f"{before} -> {myitems[str(interaction.user.id)][itempos]['lvl']}"
                    embed = ds.Embed(color=0xffaa00)
                    viewe.add_item(upgrade)
                else:
                    content = f"{before} -> {myitems[str(interaction.user.id)][itempos]['lvl']}"
                    embed = ds.Embed(color=0x00ff00)
                    viewe.add_item(upgrade)
                
                embed.title = f'{myitems[str(interaction.user.id)][itempos]["name"]} Lv.{myitems[str(interaction.user.id)][itempos]["lvl"]}'
                embed.description = myitems[str(interaction.user.id)][itempos]['description']
                
                if myitems[str(interaction.user.id)][itempos]["lvl"] == None:
                    del myitems[str(interaction.user.id)][itempos]
                with open('data\\item.json',"w") as file:
                    json.dump(myitems,file)
                    
                if str(interaction.user.id) not in items:
                    itemselect.options=[ds.SelectOption(label="현재 아무 아이템도 소지하고 있지 않아!",value="no",description="`/아이템 제작`로 아이템을 만들어줘!")]
                else:
                    itemselect.options=[ds.SelectOption(label=item["name"],value=str(item),description=item["lvl"]) for item in myitems[str(interaction.user.id)]]
                viewe.add_item(itemselect)
                await interaction.response.edit_message(content=content,embed=embed,view=viewe)
            
            upgrade.callback = itemupgrade
            viewe.add_item(upgrade)
            with open('data\\item.json', encoding="UTF8") as file:
                items = json.load(file)
            if str(interaction.user.id) not in items:
                itemselect.options = [ds.SelectOption(label="현재 아무 아이템도 소지하고 있지 않아!",value="no",description="`/아이템 제작`로 아이템을 만들어줘!")]
            else:
                itemselect.options = [ds.SelectOption(label=item["name"],value=str(item),description=item["lvl"]) for item in items[str(interaction.user.id)]]
            viewe.add_item(itemselect)
            await interaction.response.edit_message(content="",embed=embed,view=viewe)
        async def callbackn(interaction:ds.Interaction):
            await interaction.message.delete()
        
        viewd = View()
        if str(interaction.user.id) not in items:
            itemselect = Select(options=[ds.SelectOption(label="현재 아무 아이템도 소지하고 있지 않아!",value="no",description="`/아이템 제작`로 아이템을 만들어줘!")])
            itemselect.callback = callbackn
        else:
            itemselect = Select(options=[ds.SelectOption(label=item["name"],value=str(item),description=item["lvl"]) for item in items[str(interaction.user.id)]])
            itemselect.callback = callbacky
        viewd.add_item(itemselect)
        await interaction.response.send_message("정보를 원하는 아이템을 골라주세요",view=viewd,ephemeral=True)