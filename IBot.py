import discord
import sqlite3
import os
import youtube_dl
import random
import string, json
from discord.ext import commands
from config import settings
from tabulate import tabulate
conn = sqlite3.connect("IBot.db") # или :memory:
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS shop(

	"id"	INT,
	"type"	TEXT,
	"name"	TEXT,
	"cost"	INT);
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
	"id"	INT,
	"nickname"	TEXT,
	"mention"	TEXT,
	"money"	INT,
	"rep_rank"	TEXT,
	"inventory"	TEXT,
	"lvl"	INT,
	"xp"	INT);
""")
conn.commit()
bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("IBot all rights reserved")#сообщение о готовности
    for guild in bot.guilds:#т.к. бот для одного сервера, то и цикл выводит один сервер
        print(guild.id)#вывод id сервера
        for member in guild.members:#цикл, обрабатывающий список участников
            cursor.execute(f"SELECT id FROM users where id={member.id}")#проверка, существует ли участник в БД
            if cursor.fetchone()==None:#Если не существует
                cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 0, 'S','[]',0,0)")#вводит все данные об участнике в БД
            else:#если существует
                pass
            conn.commit()#применение изменений в БД

@bot.event
async def on_member_join(member):
    cursor.execute(f"SELECT id FROM users where id={member.id}")#все также, существует ли участник в БД
    if cursor.fetchone()==None:#Если не существует
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 0, 'S','[]',0,0)")#вводит все данные об участнике в БД
    else:#Если существует
        pass
    conn.commit()#применение изменений в БД


@bot.event
async def on_member_join(member):
    await member.send('Спасибо что присоеденился к нам!')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == '🌏│welcome':
            await bot.get_channel(ch.id).send(f'{member.mention} Добро пожаловать.')

@bot.command()
async def info(ctx):
    imageURL = "https://i.imgur.com/8YgFYmf.jpg"
    embed = discord.Embed(color = 0xfff5, title = 'Основные команды', description = '!info - основные команды сервера.\n !ping - сыграй с ботом.\n !twitch - официальный Twitch создателя бота.\n !join - присоеденить бота в войс.\n !play (ссылка) - включить музыку.\n !pause - остановить трэк.\n !resume - продолжить воспроизведение.\n !skip - пропустить музыку.\n !leave - прощай бот.') # Создание Embed'a
    embed.set_image(url = imageURL) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def ping(ctx):
    imageURL = "https://i.imgur.com/IYti89l.gif"
    embed = discord.Embed(color = 0xfff5, title = 'pong') # Создание Embed'a
    embed.set_image(url = imageURL) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def twitch(ctx):
    await ctx.send('Twicth - https://www.twitch.tv/deception_es')

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f'{member.mention} Вы не подключены к voice чату.')
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Ожидайте окончания песни! Или воспользуйтесь командой '!skip'")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

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
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("LimeBot не подключён к voice чату.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Музыка не проигрывается в данный момент.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("В данный момент играет музыка.")

@bot.command()
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

bot.run('ODY0MTU1Nzk2NjcyODcyNDY5.YOxVzQ.TlCiUOzlHgdeeqKlo1p-SviN8w8')
