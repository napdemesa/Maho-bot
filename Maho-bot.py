import discord

client = discord.Client()

token = input('Enter Discord bot token for Maho: ')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)