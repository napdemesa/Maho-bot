import discord
import asyncio
import random

client = discord.Client()
token = input('Enter Discord bot token for Maho: ')

while len(token) != 59:
    print('Unfortunately that token key is incorrect, please reenter the token: ')
    token = input()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('$roll'):
        roll = random.randint(1,6)
        strRoll = str(roll)
        msg = 'You rolled a {num}!'.format(message,num=strRoll)
        await client.send_message(message.channel,msg)

client.run(token)
