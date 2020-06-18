import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import asyncio

token = open("../token.txt", "r").read()  # I've opted to just save my token to a text file.
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()  # starts the discord client.
#bot = commands.Bot(command_prefix='-')
bot = commands.Bot(command_prefix='-')

@bot.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #print(f'We have logged in as {client.user}')  # notification of login.


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):  # event that happens per any message.
    if message.author == client.user:
        return
    current_guilds = client.guilds
    # each message has a bunch of attributes. Here are a few.
    # check out more by print(dir(message)) for example.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if "прикол" in message.content.lower():
        await message.channel.send('Прикол на 9/10, Серёга, так держать!')

    elif "community_report" == message.content.lower():
        online = 0
        idle = 0
        offline = 0

        for m in current_guilds[0].members:
            if str(m.status) == "online":
                online += 1
            if str(m.status) == "offline":
                offline += 1
            else:
                idle += 1

        await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```")

    elif "logout" == message.content.lower():
        await client.close()

    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
    # if "member_count" == message.content.lower():
    #     await message.channel.send(f"```{current_guilds[0].member_count}```")
    #if str(message.author) == "Quo#5043" and "hello" in message.content.lower():
    #    await message.channel.send('Hi!')


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create_channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):

    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.command(name='pages')
async def embedpages(ctx):
    page1=discord.Embed(
        title='Page 1/3',
        description='Description',
        colour=discord.Colour.orange()
    )
    page2=discord.Embed(
        title='Page 2/3',
        description='Description',
        colour=discord.Colour.orange()
    )
    page3=discord.Embed(
        title='Page 3/3',
        description='Description',
        colour=discord.Colour.orange()
    )

    pages=[page1,page2,page3]

    message=await ctx.say(embed=page1)

    await ctx.add_reaction(message,'\u23ee')
    await ctx.add_reaction(message,'\u25c0')
    await ctx.add_reaction(message,'\u25b6')
    await ctx.add_reaction(message,'\u23ed')

    i=0
    emoji=''

    while True:
        if emoji=='\u23ee':
            i=0
            await ctx.edit_message(message,embed=pages[i])
        if emoji=='\u25c0':
            if i>0:
                i-=1
                await ctx.edit_message(message,embed=pages[i])
        if emoji=='\u25b6':
            if i<2:
                i+=1
                await ctx.edit_message(message,embed=pages[i])
        if emoji=='\u23ed':
            i=2
            await ctx.edit_message(message,embed=pages[i])

        res=await ctx.wait_for_reaction(message=message,timeout=30)
        if res==None:
            break
        if str(res[1])!='Imitation of Life#6042': #Example: 'MyBot#1111'
            emoji=str(res[0].emoji)
            await ctx.remove_reaction(message,res[0].emoji,res[1])

    await ctx.clear_reactions(message)

left = ':one:'
right = ':two:'
# right1 = ':arrow_forward:'
# start = '\u23ee'
# end = '\u25c0'
# messages = ("1", "2", "3")
page1 = discord.Embed(
    title='Page 1/3',
    description='Description',
    colour=discord.Colour.orange()
)
page2 = discord.Embed(
    title='Page 2/3',
    description='Description',
    colour=discord.Colour.orange()
)
page3 = discord.Embed(
    title='Page 3/3',
    description='Description',
    colour=discord.Colour.orange()
)

messages = (page1, page2, page3)


def predicate(message, l, r):
    def check(reaction, user):
        if reaction.message.id != message.id or user == bot.user:
            return False
        if l and reaction.emoji == left:
            return True
        if r and reaction.emoji == right:
            return True
        return False

    return check


@bot.command(pass_context=True)
async def series1(ctx):
    index = 0
    while True:
        msg = await bot.say(messages[index])
        l = index != 0
        r = index != len(messages) - 1
        if l:
            await bot.add_reaction(msg, left)
        if r:
            await bot.add_reaction(msg, right)
        # bot.wait_for_reaction
        react, user = await bot.wait_for_reaction(check=predicate(msg, l, r))
        if react.emoji == left:
            index -= 1
        elif react.emoji == right:
            index += 1

        await bot.delete_message(msg)


@bot.command(pass_context=True)
async def series(ctx):
    index = 0
    msg = None
    action = ctx.send
    while True:
        res = await action(embed=messages[index])
        if res is not None:
            msg = res
        l = index != 0
        r = index != len(messages) - 1
        if l:
            await msg.add_reaction(left)
        if r:
            await msg.add_reaction(right)
        react, user = await bot.wait_for('reaction_add', check=predicate(msg, l, r))
        if react.emoji == left:
            index -= 1
        elif react.emoji == right:
            index += 1
        # elif react.emoji == start:
        #     index = 0
        # elif react.emoji == end:
        #     index = -1
        action = msg.edit


@bot.command(name='logout')
async def on_logout(ctx):
    await bot.close()

loop = asyncio.get_event_loop()
task1 = loop.create_task(bot.start(TOKEN))
task2 = loop.create_task(client.start(TOKEN))
gathered = asyncio.gather(task1, task2, loop=loop)
loop.run_until_complete(gathered)



#loop.run_forever()


#bot.run(TOKEN)  # recall my token was saved!
# client.run(TOKEN)
# @bot.command()
# async def ping(ctx):
#     await ctx.send('pong')

# bot.run('NzIzMTE1NzI3NTE0NTAxMTgx.XutAHw.YpTRsGvnpiSOfBz__HNqw7J9tPs')
