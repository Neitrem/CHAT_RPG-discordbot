import discord
from discord.ext import commands
from main import CreateTable, AddNewPLayerToDB, CreateCharacterInfoMessage

token = open('token.txt', 'r').readline().split('=')[1]
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    CreateTable()
    print('Table have been created.')


@bot.command(name='test') # use it to create any new command
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command(name='start')
async def start(ctx):
    result = AddNewPLayerToDB(ctx.author.id) # 0 - success, 1 - fail
    if result:
        print(f'Registration failed: {ctx.author.id} already have account!')
        await ctx.send("You already have account!\n"
                       "Type `ch` to observe your character info.")
    else:
        print(f'Registration for {ctx.author.id} is successful.')
        await ctx.send("Your account was created successfully.\n"
                       "Type `ch` to observe your character info.")


@bot.command(name='ch')
async def ShowCharacterInfo(ctx):
    emb = discord.Embed(color=discord.Color.dark_gray())
    emb.add_field(name='Main character info:', value=CreateCharacterInfoMessage(ctx.author.id))
    await ctx.send(embed=emb)


bot.run(token)
