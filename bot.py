import discord
from discord.ext import commands
import datetime
import config
import requests
import json
import datetime
from discord.utils import get



api_key = "токен"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

client = commands.Bot( command_prefix = "$" , intents = discord.Intents.all())
client.remove_command( "help" )
# Word
hello_words = [ "Привет", "ку", "ку-ку","hi", "hello", "ky","привет" ] 
answer_words = [ "инфо", "узнать информацию", "информация ","команды"  ]
goodbue_words = [ "пока", "poka", "bye", "bb", "я пошел", "досвидос", "до скорой встречи", ]
bad_words = [ "кик" , "флуд", "бан"]
@client.event

async def on_ready():
	print("Бот активен")

	await client.change_presence( status = discord.Status.online, activity = discord.Game( " $help ") ) 

@client.event
async def on_command_error(ctx, error ):
	pass

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

#удаление команд

@client.command()


async def hello ( ctx, amount = 1 ):
	await ctx.channel.purge( limit = amount )

	author = ctx.message.author
	await ctx.send( F"Привет { author.mention }" )

#кик 

@client.command()
@commands.has_permissions( administrator = True)

async def kick(ctx , member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send( f"Кикнут { member.mention }" )


#бан 

@client.command()
@commands.has_permissions( administrator = True)

async def ban(ctx , member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )
	await ctx.send( f"Забанен { member.mention }" )

#help 
@client.command()


async def help( ctx ): 
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = "Навигатор по командам" )

	emb.add_field ( name = '{}clear'.format ( "$" ), value = "Очистка чата" )
	emb.add_field ( name = '{}ban'.format ( "$" ), value = "Блокировка пользователя" )
	emb.add_field ( name = '{}kick'.format ( "$" ), value = "Кик пользователя" )
	emb.add_field ( name = '{}mute'.format ( "$" ), value = "ограничение пользователя" )
	emb.add_field ( name = '{}av'.format ( "$" ), value = "Получение аватарки пользователя" )
	emb.add_field ( name = '{}serverinfo'.format ( "$" ), value = "Получение info о сервере" )
	emb.add_field ( name = '{}hello'.format ( "$" ), value = "Приветствие " )
	emb.add_field ( name = '{}weather'.format ( "$" ), value = "Погода + город " )
	emb.add_field ( name = '{}fox'.format ( "$" ), value = "Рандомные картинки лис" )
	emb.add_field ( name = '{}bird'.format ( "$" ), value = "Рандомные картинки птиц" )
	emb.add_field ( name = '{}pikachu'.format ( "$" ), value = "Рандомные картинки пикачу" )
	emb.add_field ( name = '{}cat'.format ( "$" ), value = "Рандомные картинки котиков" )


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
@commands.has_permissions( administrator = True)

async def mute(ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = "mute"  )

	await member.add_roles (mute_role )
	await ctx.send( f"Пользователь { member.mention }, замучен за нарушение правил чата")


#Фильтер
@client.event
async def on_message( message ):
	await client.process_commands( message )

	msg = message.content.lower()

	if msg in bad_words:
		await message.delete()
		await message.author.send(f'{message.author.mention}, лучше не нужно писать такое! ')




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

@mute.error
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

#join к голосовым чатам

@client.command()
async def join(ctx):
	global voice 
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else: 
		voice = await channel.connect()
		await ctx.send(f'Бот успешно подключен к {channel}')


#leave из голосовым чатам

@client.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else: 
		voice = await channel.connect()
		await ctx.send(f'Бот успешно вышел из {channel}')





#connect 

client.run(config.TOKEN) 
