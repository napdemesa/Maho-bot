import discord
import asyncio
import random


class Maho(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_message(self, message):
		channel = message.channel
		if message.author == self.user:
			return

		if message.content.startswith('$hello'):
			msg = 'Hello {0.author.mention}'.format(message)
			await channel.send(msg)

		if message.content.startswith('$roll'):
			roll = random.randint(1,6)
			strRoll = str(roll)
			msg = 'You rolled a {num}!'.format(message,num=strRoll)
			await channel.send(msg)

		if message.content.startswith('$mcss'):
			pass
