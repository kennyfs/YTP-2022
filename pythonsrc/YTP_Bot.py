import os
import discord
from dotenv import load_dotenv

imagePath = "/home/astrayt/YTP2022/"  # default path on someone's computer


def run(imageFile):
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        if message.content == "amogus":
            await message.channel.send("sus")
            
        if message.content == ">news":
            await message.channel.send("本日新聞統整")
            with open(
                imageFile,
                "rb",
            ) as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        
        if message.content == ">help":
            await message.channel.send(">news 查看新聞統整圖片\n圖片顏色說明：紅色―出現次數頻繁、藍色—與其他詞大量連接、紫色—同時滿足藍色與紅色")

    client.run("TOKEN")
