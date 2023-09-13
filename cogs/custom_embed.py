from typing import Optional
import discord as ds
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal,View,TextInput,Button
from discord.utils import MISSING

async def add_embed_field(interaction:ds.Interaction,embed:ds.Embed):
    modal = Modal(title="필드 추가")
    
    field_name = TextInput(label="field name",placeholder="필드 이름",)
    modal.add_item(field_name)
    field_value = TextInput(label="field value",placeholder="필드 내용",)
    modal.add_item(field_value)
    
    async def on_submits(interaction:ds.Interaction):
        embed.add_field(name=field_name.value,value=field_value.value)
        await interaction.response.edit_message(embed=embed)
    modal.on_submit = on_submits
    
    await interaction.response.send_modal(modal)

async def change_color(interaction:ds.Interaction,embed:ds.Embed):
    modal = Modal(title="색상 변경")
    
    embed_color = TextInput(label="color",placeholder="ex) ffa4c6")
    modal.add_item(embed_color)

    async def on_submits(interaction:ds.Interaction):
        embed.color = int(embed_color.value,16)
        await interaction.response.edit_message(embed=embed)
    modal.on_submit = on_submits
    
    await interaction.response.send_modal(modal)

class CustomEmbed(commands.Cog):
    g_embed = app_commands.Group(name="임베드",description="임베드")
    
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
        
    @g_embed.command(name="만들기",description="임베드를 커스텀해서 보낼 수 있습니다")
    @app_commands.describe(title="임베드 최상단의 제목입니다")
    @app_commands.describe(description="임베드 최상단의 설명입니다")
    async def make_embed(self,interaction:ds.Interaction,title:str,description:str):
        embed = ds.Embed(title=title,description=description)
        view = View()
        
        add_field = Button(label="➕추가하기")
        async def add_field_callback(interaction:ds.Interaction):
            await add_embed_field(interaction,embed)
        add_field.callback = add_field_callback
        
        change_colors = Button(label="🌈색상변경")
        async def change_color_callback(interaction:ds.Interaction):
            await change_color(interaction,embed)
        change_colors.callback = change_color_callback
        
        return_embed = Button(style=ds.ButtonStyle.green,label="✅보내기")
        async def return_embed_callback(interaction:ds.Interaction):
            await interaction.channel.send(embed=interaction.message.embeds[0])
            await interaction.response.edit_message(content="\u3164",embed=None,view=None)
        return_embed.callback = return_embed_callback
        
        view.add_item(add_field)
        view.add_item(change_colors)
        view.add_item(return_embed)
        
        await interaction.response.send_message(embed=embed,view=view,ephemeral=True)