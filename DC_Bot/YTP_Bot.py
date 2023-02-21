import os
import discord
from dotenv import load_dotenv

imagePath = "c:/Users/Astrayt.DESKTOP-S6089ME/Desktop/YTP-2022/output.jpg"  # default path on someone's computer


if __name__ == "__main__":
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
            with open(
                imagePath,
                "rb",
            ) as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

    client.run("TOKEN")
