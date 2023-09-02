import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button, ChannelSelect

import json

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
            viewe.add_item(upgrade)
            viewe.add_item(itemselect)
            await interaction.response.edit_message(embed=embed,view=viewe)
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