import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("MTA2OTkzNjUyMTA2ODY5NTYwMg.G1pjdV.ioqYUlLD7StkxXo0e6YNM3wTFkkkCRaoIFobRI")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    if message.author == client.user :
        return
    if message.content == 'amogus' :
        await message.channel.send('sus')
    if message.content == '>news' :
        await message.channel.send('No news for you, bitch')

client.run("MTA2OTkzNjUyMTA2ODY5NTYwMg.G1pjdV.ioqYUlLD7StkxXo0e6YNM3wTFkkkCRaoIFobRI")