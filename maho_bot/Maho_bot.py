import discord
import asyncio
import random
import boto3
from botocore.exceptions import ClientError
import json
import sys
import os

sys.path.insert(0, '/home/ec2-user/Maho-bot/ec2_instance_control')
import turn_instance_on as ec2
sys.path.insert(0, '/home/ec2-user/Maho-bot/mc_server')
import turn_mc_server_on as mcs
import youtube_dl

from discord.ext import commands


def get_instance_id(path):
	ssm = boto3.client('ssm')
	args = {"Name": path, "WithDecryption": True}
	try:
		param = ssm.get_parameter(Name=path, WithDecryption=True)
	except ClientError as e:
		if e.response['Error']['Code'] == 'ParameterNotFound':
			print('Parameter does not exist')
		else:
			print('parameter exists')

	return json.loads(param['Parameter']['Value'])


creds = get_instance_id('minecraft')
intents = discord.Intents().all()
maho = commands.Bot(command_prefix='$', intents=intents)


@maho.event
async def on_ready():
	print('Logged on as {0}!'.format(maho.user))


@maho.event
async def on_message(message):
	channel = message.channel
	if message.author == maho.user:
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
			await channel.send('''Instance is now online! DO NOT TURN SERVER ON DUDE! Just like a computer, a server needs to boot up! Wait at least 30 seconds before trying to turn the minecraft server on to prevent any issues with the AWS instance!''')
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
		instance_status, instance_message, instance_ip = ec2.check_instance_status()
		mcss, message = mcs.check_minecraft_server_status(instance_ip[4:])
		await channel.send(message)

	if message.content.startswith('$mc_server_on'):
		await channel.send('Attempting to turn server on...')
		try:
			instance_status, instance_message, instance_ip = ec2.check_instance_status()
			server_status, message = mcs.turn_server_on(instance_status, instance_ip[4:])
			if server_status:
				await channel.send('The server is now online!')
				await channel.send(message)
		except Exception:
			await channel.send("Couldn't turn server on.")
			await channel.send(message)
	
	await maho.process_commands(message)


@maho.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@maho.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice = discord.utils.get(maho.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@maho.command(name='play')
async def play(ctx, url : str):
	voice = discord.utils.get(maho.voice_clients, guild=ctx.guild)
	is_song_there = os.path.isfile('song.mp3')
	try:
		if is_song_there:
			os.remove('song.mp3')
	except PermissionError:
		await ctx.send('Wait for song to end or use command $stop')

	ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("/home/ec2-user/Maho-bot/maho_bot"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
	voice.play(discord.FFmpegPCMAudio("song.mp3"))


@maho.command(name='pause')
async def pause(ctx):
	voice = discord.utils.get(maho.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		await voice.pause()
	else:
		await ctx.send("The bot is not playing anything at the moment.")
    
@maho.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(maho.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@maho.command(name='stop')
async def stop(ctx):
    voice = discord.utils.get(maho.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


maho.run(creds['maho_bot_token'])