import discord
import asyncio
import random
import sys

sys.path.insert(0, '/Users/nap/maho/Maho-bot/ec2_instance_control')
import turn_instance_on as ec2
sys.path.insert(0, '/Users/nap/maho/Maho-bot/mc_server')
import turn_mc_server_on as mcs


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

		if message.content.startswith('$ec2'):
			instance_status, instance_message, instance_ip = ec2.check_instance_status()
			msg = '{ime}; {iip}'.format(message, ime=instance_message, iip=instance_ip)
			await channel.send(msg)
		
		if message.content.startswith('$turn_instance_on'):
			await channel.send('Attempting to turn server on...')
			turn_instance_on, response= ec2.turn_instance_on()
			if turn_instance_on:
				await channel.send('Instance is now online!')
			else:
				msg = 'Instance did not turn on... Please inform nap. \n{mess}'.format(message, mess=response)
				await channel.send(msg)
		
		if message.content.startswith('$turn_instance_off'):
			await channel.send('Attempting to turn server off...')
			turn_instance_off, response = ec2.turn_instance_off()
			if turn_instance_off:
				await channel.send('Instance is now offline!')
			else:
				msg = 'Instance did not turn off... Please inform nap. \n{mess}'.format(message, mess=response)
				await channel.send(msg)
		
		if message.content.startswith('$mcss'):
			mcss, message = mcs.check_minecraft_server_status()
			await channel.send(message)

		if message.content.startswith('$mc_server_on'):
			try:
				instance_status, instance_message, instance_ip = ec2.check_instance_status()
				server_status, message = mcs.turn_server_on(instance_status, instance_ip)
				if server_status:
					await channel.send('The server is now online!')
					await channel.send(message)
			except Exception:
				await channel.send("Couldn't turn server on.")

