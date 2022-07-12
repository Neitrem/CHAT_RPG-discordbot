import discord
from discord.ext import commands
from main import *

token = open('token.txt', 'r').readline().split('=')[1]
bot = commands.Bot(command_prefix='!')

SUCCESS = discord.Color.from_rgb(0, 255, 0)
INFO = discord.Color.from_rgb(169, 169, 169)
WARN = discord.Color.from_rgb(255, 165, 0)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    CreateTable()
    print('Table have been created.')


@bot.command(name='test')  # use it to create any new command
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command(name='start')
async def _start(ctx):
    result = AddNewPLayerToDB(ctx.author.id)  # 0 - success, 1 - fail
    if result:
        print(f'Registration failed: {ctx.author.id} already have account!')
        await ctx.send("You already have account!\n"
                       "Type `ch` to observe your character info.")
    else:
        print(f'Registration for {ctx.author.id} is successful.')
        await ctx.send("Your account was created successfully.\n"
                       "Type `ch` to observe your character info.")


@bot.command(name='ch')
async def _ShowCharacterInfo(ctx):
    emb = discord.Embed(color=INFO)
    player = GetPlayerFromDB(ctx.author.id)
    emb.add_field(name='Main character info:', value=player.CreateCharacterInfoMessage())
    await ctx.send(embed=emb)


@bot.command(name='inv')
async def _ShowInventory(ctx, arg=1):
    emb = discord.Embed(color=INFO)
    player = GetPlayerFromDB(ctx.author.id)
    emb.add_field(name=f'Character inventory page {arg}:', value=player.CreateInventoryListMessage(arg))
    await ctx.send(embed=emb)


@bot.command(name='eqvt')
async def _EquipTool(ctx, num=None):
    player = GetPlayerFromDB(ctx.author.id)
    res, text = EquipTool(ctx.author.id, player, int(num)-1)
    if res == 0:
        emb = discord.Embed(color=SUCCESS)
    else:
        emb = discord.Embed(color=WARN)
    emb.add_field(name=f'Event info: ', value=text)
    await ctx.send(embed=emb)


@bot.command(name='eqvc')
async def _EquipClothes(ctx, num=None):
    player = GetPlayerFromDB(ctx.author.id)
    res, text = EquipClothes(ctx.author.id, player, int(num) - 1)
    if res == 0:
        emb = discord.Embed(color=SUCCESS)
    else:
        emb = discord.Embed(color=WARN)
    emb.add_field(name=f'Event info: ', value=text)
    await ctx.send(embed=emb)


@bot.command(name='deqvc')
async def _dEquipClothes(ctx, body_part=None):
    player = GetPlayerFromDB(ctx.author.id)
    res, text = DeEquipClothes(ctx.author.id, player, body_part)
    if res == 0:
        emb = discord.Embed(color=SUCCESS)
    else:
        emb = discord.Embed(color=WARN)
    emb.add_field(name=f'Event info: ', value=text)
    await ctx.send(embed=emb)


@bot.command(name='deqvt')
async def _dEquipTools(ctx):
    player = GetPlayerFromDB(ctx.author.id)
    res, text = DeEquipTool(ctx.author.id, player)
    if res == 0:
        emb = discord.Embed(color=SUCCESS)
    else:
        emb = discord.Embed(color=WARN)
    emb.add_field(name=f'Event info: ', value=text)
    await ctx.send(embed=emb)


bot.run(token)
