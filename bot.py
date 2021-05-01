import datetime
import config
import json
from discord.utils import get
import sys
import discord # Импорт главной библиотеки discord.py
import json # Работа с файлами
import requests # Работа с запросами
import asyncio # Работа с музыкой
import youtube_dl # Скачивание музыки с yt
import functools # Вспомогательный функционал
import itertools # Вспомогательный функционал
import math # Математика
import random # Рандом
import ffmpeg # Проигрывание музыки
import colorsys # Система цветов
import glob
import os
from discord.ext import commands
import glob
import discord
from random import randint, choice
from discord.ext import commands
import datetime, pyowm

from discord.utils import get
import youtube_dl
 
import os
from time import sleep
import requests
from PIL import Image, ImageFont, ImageDraw
import io
import asyncio
from os import walk
from discord.ext import commands
from collections.abc import Sequence


api_key = "токен"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

client = commands.Bot( command_prefix = "$" , intents = discord.Intents.all())
client.remove_command( "help" )
# Word
hello_words = [ "Привет", "ку", "ку-ку","hi", "hello", "ky","привет" ] 
answer_words = [ "инфо", "узнать информацию", "информация ","команды"  ]
goodbue_words = [ "пока", "poka", "bye", "bb", "я пошел", "досвидос", "до скорой встречи", ]


@client.event

async def on_ready():
	print("Бот активен")

	await client.change_presence( status = discord.Status.online, activity = discord.Game( " $help ") ) 

#help

@client.command(aliases = ['help', 'Help', 'помощь', 'хелп'])
async def __help(ctx):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = "Навигатор по командам :clipboard:" )

	emb.add_field ( name = '{}clear'.format ( "$" ), value = "Очистка чата" )
	emb.add_field ( name = '{}ban'.format ( "$" ), value = "Блокировка пользователя" )
	emb.add_field ( name = '{}kick'.format ( "$" ), value = "Кик пользователя" )
	emb.add_field ( name = '{}unban'.format ( "$" ), value = "Разблокировка пользователя" )
	emb.add_field ( name = '{}av'.format ( "$" ), value = "Получение аватарки пользователя" )
	emb.add_field ( name = '{}serverinfo'.format ( "$" ), value = "Получение info о сервере" )

	emb.add_field ( name = '{}weather'.format ( "$" ), value = "Погода + город " )
	emb.add_field ( name = '{}fox'.format ( "$" ), value = "Рандомные картинки лис" )
	emb.add_field ( name = '{}bird'.format ( "$" ), value = "Рандомные картинки птиц" )
	emb.add_field ( name = '{}pikachu'.format ( "$" ), value = "Рандомные картинки пикачу" )
	emb.add_field ( name = '{}cat'.format ( "$" ), value = "Рандомные картинки котиков" )
	emb.add_field ( name = '{}ran'.format ( "$" ), value = "Рандомная цифра и 2-ух значное число" )
	emb.add_field ( name = '{}coin'.format ( "$" ), value = "Подбросить монетку" )
	emb.add_field ( name = '{}rps'.format ( "$" ), value = "Камень-ножницы-бумага" )
	emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/alecive/flatwoken/128/Apps-Help-icon.png")

	await ctx.send( embed = emb )


@client.event

async def on_message ( message ):
	await client.process_commands( message )
	msg = message.content.lower()

	if msg in hello_words: 
		await message.channel.send( "Привет, что хотел? Бот находится на стадии разработки... Можешь посмотреть список доступныйх команд $help ")

	if msg in answer_words: 
		await message.channel.send(" Я тебя понял, но лучше прописать !help , там все подробно написанно ")

	if msg in goodbue_words: 
		await message.channel.send("Пока, жду нового общения с тобой :)")
#удаление сообщений просто команда $clear чистит 1 смс, после $clear надо указать кол-во 
 
@client.command()
@commands.has_permissions( administrator = True)

async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)

	await ctx.send(embed = discord.Embed(description = f":white_check_mark: Удалено {amount} сообщений", color=ctx.guild.me.top_role.color))


# Kick
@client.command()
@commands.has_permissions( administrator = True )
 
async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.kick( reason = reason )
 
    emb = discord.Embed( title = 'Информация об изгнании', description = f'{ member.name.title() }, был выгнан в связи нарушений правил',
    color = 0xc25151 )
 
    emb.set_author( name = member, icon_url = member.avatar_url )
    emb.set_footer( text = f'Был изганан администратором { ctx.message.author.name }', icon_url = ctx.author.avatar_url )
 
    await ctx.send( embed = emb )
 
#бан 

@client.command()
@commands.has_permissions( administrator = True )
 
async def ban( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.ban( reason = reason )
 
    emb = discord.Embed( title = 'Информация о блокировке участника', description = f'{ member.name }, был заблокирован в связи нарушений правил',
    color = 0xc25151 )
 
    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = f'ID: { member.id }', value = f'Блокированный участник : { member }' )
    emb.set_footer( text = 'Был заблокирован администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
 
    await ctx.send( embed = emb )
 
#unban 
@client.command()
@commands.has_permissions( ban_members = True )

async def unban(ctx, user_id: int):
	await ctx.channel.purge( limit = 1 )
	user = await client.fetch_user(user_id)
	await ctx.guild.unban(user)

	emb = discord.Embed( title = 'Информация о разблокировке участника', description = f'{ user.name }, был разблокирован ',
	color = 0xc25151 )

	emb.set_author( name = user.name, icon_url = user.avatar_url )
	emb.add_field( name = f'ID: { user.id }', value = f'Разблокированный участник : { user }' )
	emb.set_footer( text = 'Был разблокирован администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

#weather 
@client.command()
async def weather(ctx, *, city: str):
	await ctx.channel.purge( limit = 1 )
	city_name = city
	complete_url = base_url + "appid=" + api_key + "&q=" + city
	response = requests.get(complete_url)
	x = response.json()
	channel = ctx.message.channel
	if x["cod"] != "404":
		async with channel.typing():
			y = x["main"]
			current_temperature = y["temp"]
			current_temperature_celsiuis = str(round(current_temperature - 273.15))
			current_pressure = y["pressure"]
			current_humidity = y["humidity"]
			z = x["weather"]
			weather_description = z[0]["description"]
			embed = discord.Embed(title=f"Weather in {city_name}",
								color=ctx.guild.me.top_role.color,
								timestamp=ctx.message.created_at,)
			embed.add_field(name="Описание", value=f"**{weather_description}**", inline=False)
			embed.add_field(name="Температура(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
			embed.add_field(name="Влажность(%)", value=f"**{current_humidity}%**", inline=False)
			embed.add_field(name="Атмосферное давление(hPa)", value=f"**{current_pressure}hPa**", inline=False)
			embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
			embed.set_footer(text=f"Requested by {ctx.author.name}")

			await ctx.send(embed=embed)
	else:
		await channel.send("Город не найден, попробуйте еще раз")

#рандом изображение лисы 

@client.command()
async def fox(ctx):
	await ctx.channel.purge( limit = 1 )
	response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = discord.Embed(color = 0xff9900, title = 'Рандомная лиса') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed

#рандом изображение птицы 
@client.command()
async def bird(ctx):
	await ctx.channel.purge( limit = 1 )
	response = requests.get('https://some-random-api.ml/img/birb') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = discord.Embed(color = 0xff9900, title = 'Рандомная птица') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed

#рандомный пикачу

@client.command()
async def pikachu(ctx):
	await ctx.channel.purge( limit = 1 )
	response = requests.get('https://some-random-api.ml/img/pikachu') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = discord.Embed(color = 0xff9900, title = 'Рандомный пикачу') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed

#рандомный пикачу

@client.command()
async def cat(ctx):
	await ctx.channel.purge( limit = 1 )
	response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
	json_data = json.loads(response.text) # Извлекаем JSON

	embed = discord.Embed(color = 0xff9900, title = 'Рандомный кот') # Создание Embed'a
	embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	await ctx.send(embed = embed) # Отправляем Embed

#получение аватара 

@client.command(name = "avatar", aliases =["Avatar", "av"])
async def av_cmd(ctx, user: discord.Member):
	await ctx.channel.purge( limit = 1 )
	mbed = discord.Embed(
		color = discord.Color(0xffff), 
		title = f"{user}"
		)
	mbed.set_image(url=f"{user.avatar_url}")
	await ctx.send(embed = mbed)

#получение инфо о сервере

@client.command(name = "serverinfo", aliases =["ServerINFO", "servinfo"])
async def si_cmd(ctx):
	await ctx.channel.purge( limit = 1 )
	mbed = discord.Embed(
		color = discord.Color(0xffff), 
		title = f"{ctx.guild.name}"
	)
	mbed.set_image(url = f"{ctx.guild.icon_url}")
	mbed.add_field(name = "Регион", value = f"{ctx.guild.region}")
	mbed.add_field(name = "Количество участников", value = F'{ctx.guild.member_count}' )
	mbed.set_footer(icon_url = f"{ctx.guild.icon_url}", text = f"ID канала: {ctx.guild.id}")
	await ctx.send(embed = mbed)

#Приветствие новых участников сервера 

@client.event
async def on_member_join(member):
    mbed = discord.Embed(
        color = discord.Color.magenta(),
        title = 'Приветствуем тебя',
        description = f'Привет {member.mention}, рады тебя видеть, напиши $help для просмотра команд'
    )
    await member.send(embed=mbed)


#mute 
@client.command()
 
async def time( ctx ):
    emb = discord.Embed( title = 'ВРЕМЯ', description = 'Вы сможете узнать текущее время', colour = discord.Color.green(), url = 'https://www.timeserver.ru' )
 
    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = 'Спасибо за использование нашего бота!' )
    emb.set_thumbnail( url = 'https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.jpg' )
 
    now_date = datetime.datetime.now()
 
    emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )
 
    await ctx.author.send( embed = emb )
 

#если недостаточно прав

@clear.error
async def clear_error( ctx, error):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f"{ctx.author.mention},обязательно укажите кол-во сообщений, которые хотите удалить ") 
	if isinstance( error, commands.MissingPermissions):
		await ctx.send( f"{ ctx.author.mention}, у вас недостаточно прав!" )


@ban.error
async def ban__error( ctx, error):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f"{ctx.author.mention},обязательно укажите пользователя " ) 
	if isinstance( error, commands.MissingPermissions):
		await ctx.send( f"{ ctx.author.mention}, у вас недостаточно прав!" )


@kick.error
async def ban__error( ctx, error):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f"{ctx.author.mention},обязательно укажите пользователя " ) 
	if isinstance( error, commands.MissingPermissions):
		await ctx.send( f"{ ctx.author.mention}, у вас недостаточно прав!" )


# Рандомное число
def roll_convert(argument):
    intarg = int(argument)
    switcher = {
        1: ":one:",
        2: ":two:",
        3: ":three:",
        4: ":four:",
        5: ":five:",
        6: ":six:",
        7: ":seven:",
        8: ":eight:",
        9: ":nine:",
        0: ":zero:"
    }
    return switcher.get(intarg, "what")

@client.command()
async def ran(ctx):
	r = str(random.randrange(1, 101))
	mes = ''
	for m in r:
		mes += roll_convert(m)
		await ctx.send(mes)

# Коинфлип
@client.command()
async def coin(ctx):
    r = random.randrange(1, 101)
    if r > 5:
        d = random.randrange(1, 3)
        if d == 1:
            await ctx.send(f"{ ctx.author.mention}, у вас Орёл :full_moon: ")
        else:
            await ctx.send(f"{ ctx.author.mention}, у вас Решка :new_moon: ")

    else:
        await ctx.send(':last_quarter_moon:')


#камень 
# удаление созданного канала по id
async def delete_channel(guild, channel_id):
        channel = guild.get_channel(channel_id)
        await channel.delete()

# создание нового канала в определённой категории
async def create_text_channel(guild, channel_name):
        category = get_category_by_name(guild, "Игровые комнаты") # Игровые комнаты - категория
        await guild.create_text_channel(channel_name, category=category)
        channel = get_channel_by_name(guild, channel_name)
        return channel

# получение первого канала с заданным именем
def get_channel_by_name(guild, channel_name):
    channel = None
    for c in guild.channels:
        if c.name == channel_name:
            channel = c
            break
    return channel

# получение первой категории по заданному имени
def get_category_by_name(guild, category_name):
    category = None
    for c in guild.categories:
        if c.name == category_name:
            category = c
            break
    return category

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

# https://stackoverflow.com/questions/55811719/adding-a-check-issue/55812442#55812442

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check

# Класс игры Камень-Ножницы-Бумага
class RPS:
    def __init__(self, client, channel_orig, channel, member1, member2, guild):
        self.client = client
        self.channel_orig = channel_orig # канал, в котором мы начинали новую игру
        self.channel = channel # созданный канал текущей игры
        self.member1 = member1 # первый игрок
        self.member2 = member2 # второй игрок
        self.m1_choice = 0 # выбор первого игрока
        self.m2_choice = 0 # выбор второго игрока
        self.guild = guild
        self.winner = None # будущий победитель
        # 0 - nothing; 1 - rock; 2 - paper; 3 - si.
    
    async def start(self):
        # Начало игры - пишем в лс игрокам
        await self.channel_orig.send('Началась новая игра между {} и {} !'.format(self.member1.name, self.member2.name))
        await self.member1.send('{} - {} | Введите номер фигуры: 1 - камень; 2 - ножницы; 3 - бумага.'.format(self.member1.name, self.member2.name))
        await self.member2.send('{} - {} | Ждём ход первого игрока..'.format(self.member1.name, self.member2.name))
        await self.play()
    
    async def end(self):
        # Выбор лузера
        loser = ''
        if (self.winner != self.member1):
            loser = self.member1
        else:
            loser = self.member2

        # Проверяем на ничью
        if (self.winner != '='):
            # объявляем победителя
            await self.channel_orig.send('{} победил в игре против {}'.format(self.winner, loser))
            await self.winner.send('Поздаравляю, вы победили!')

            if (self.winner != self.member1):
                await self.member1.send('К сожалению, вы проиграли :(')
            else:
                await self.member2.send('К сожалению, вы проиграли :(')
        else:
            # объявляем ничью
            await self.channel_orig.send('Ничья в игре {} против {}'.format(self.member1, self.member2))
            await self.member1.send('Ничья!')
            await self.member2.send('Ничья!')
        
        # удаляем созданный ранее канал
        await delete_channel(self.guild, self.channel.id)

    async def play(self):
        played = False
        while played == False:
            
            # что будем ожидать в ответ на ПМ от бота
            content = ('1', '2', '3')

            # ожидание ответа от первого игрока
            msg1_wait = await self.client.wait_for("message", check=message_check(channel=self.member1.dm_channel, content=content))
            # получили ответ от первого игрока, начинаем ждать 2 игрока
            await self.member1.send('{} - {} | Ждём ход второго игрока..'.format(self.member1.name, self.member2.name))
            
            # ждём ответ от 2 игрока
            await self.member2.send('{} - {} | Введите номер фигуры: 1 - камень; 2 - ножницы; 3 - бумага.'.format(self.member1.name, self.member2.name))
            msg2_wait = await self.client.wait_for("message", check=message_check(channel=self.member2.dm_channel, content=content))

            # преваращаем сообщения игроков в текст
            msg1 = msg1_wait.content
            msg2 = msg2_wait.content

            # превращаем выбор(string) игроков в выбор(int)
            self.m1_choice = int(msg1)
            self.m2_choice = int(msg2)

            # shitcode meme, case for losers, yeah
            # можете попробовать сами придумать формулу для определения победителя, мне порядком лень :c

            if (self.m1_choice == self.m2_choice):
                self.winner = '='
            if (self.m1_choice == 1) and (self.m2_choice == 2):
                self.winner = self.member1
            if (self.m2_choice == 1) and (self.m1_choice == 2):
                self.winner = self.member2
            if (self.m1_choice == 2) and (self.m2_choice == 3):
                self.winner = self.member1
            if (self.m2_choice == 2) and (self.m1_choice == 3):
                self.winner = self.member2
            if (self.m1_choice == 3) and (self.m2_choice == 1):
                self.winner = self.member1
            if (self.m2_choice == 3) and (self.m1_choice == 1):
                self.winner = self.member2

            # выходим из цикла (while not played...)
            played = True
        
        # переходим к завершению игры
        await self.end()


# Получаем сообщение о создании игры
@client.command(aliases = ['rps', 'камень ножницы бумага', 'кнб', 'RPS', 'Rps', 'Кнб', 'КНБ'])
async def __rps(ctx, member_name=''):

    if member_name == '':
        await ctx.send('Укажите никнейм оппонента и его хештег ($rps Nickname)')
        return 0
  
    # ищем игрока по маске (nickname + tag)
    member = None
    async for mem in ctx.guild.fetch_members(limit=None):
        if (mem.name.find(member_name) > -1):
            member = mem
            break

    # сообщаем, что не нашли пользователя
    if not member:
        await ctx.send('Не удалось найти пользователя')
        return 0
    
    # member == author
    if member == ctx.message.author:
        await ctx.send('Вы не можете учавствовать в игре с самим собой')
        return 0

    # member == bot
    if member.bot:
        await ctx.send('Бот не может участвовать в играх')
        return 0
    
    # 2 чаннела для проверки активной игры между двумя игрокам с разных сторон
    channel_name = ctx.message.author.name + '-' + member.name
    channel_name = channel_name.replace(' ', '-')
    channel_name = channel_name.lower()
    channel = get_channel_by_name(ctx.message.channel.guild, channel_name)

    channel_name2 = member.name + '-' + ctx.message.author.name
    channel_name2 = channel_name2.replace(' ', '-')
    channel_name2 = channel_name2.lower()
    channel2 = get_channel_by_name(ctx.message.channel.guild, channel_name2)

    # если ни один из каналов не существует (нет активной игры), то создаём
    if (not channel) and (not channel2):
        # создаём канал
        new_channel = await create_text_channel(ctx.message.channel.guild, channel_name)
        game = RPS(client, ctx.message.channel, new_channel, ctx.message.author, member, ctx.message.channel.guild)

        # переходим к началу игры
        await game.start()
    else:
        await ctx.send('У вас уже идёт активная игра')
        return 0

#connect 
client.run(config.TOKEN) 
