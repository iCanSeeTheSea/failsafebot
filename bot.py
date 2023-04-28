# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import choice
import time

bootTime = time.localtime()

# logFile = open(f'logs/{time.strftime("%Y-%m-%d_%H.%M.%S", bootTime)}.txt', 'w+')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MY_ID = int(os.getenv('MY_ID'))

# craigSimp = [
#     ':blush: hi Craig! :heart_eyes::kissing_closed_eyes:',
#     ':star_struck: OMG guys it\'s Craig!! :star_struck:',
#     ':sparkles::sparkling_heart::smiling_face_with_3_hearts: I LOVE YOU CRAIG!!!! :sparkles::sparkling_heart::smiling_face_with_3_hearts:'
# ]

bonkGifs = ['https://tenor.com/view/statewide-rp-mess-with-the-honk-you-get-the-bonk-baseballbat-untitled-goose-game-gif-17204101',
            'https://tenor.com/view/mihoyo-genshin-genshin-impact-paimon-you-deserved-gif-23340767',
            'https://tenor.com/view/chikku-neesan-girl-hit-wall-stfu-anime-girl-smack-gif-17078255',
            'https://tenor.com/view/anime-bonk-gif-22497698',
            'https://tenor.com/view/horny-bonk-gif-22415732',
            'https://tenor.com/view/no-horny-gura-bonk-gif-22888944']

ntf_messages = {}

help_messages = {'standard': '''```
Available commands:
    - pingme
    - bonk
    - ntf
For more information about a command, try \\help <command>.
```''',
                 'pingme': '`Pingme: literally just pings you.`',
                 'bonk': '''```
Bonk: pings a user a certain number of times.
    \\bonk <@user> <number of times> <message>
- Leaving <number of times> blank will ping once.
- Leaving <message> blank will send a random bonk-related gif.
```''',
                 'ntf': '''```
Notify: pings a user/s with any message as a spoiler. When everyone pinged reacts with ✅ the message is deleted.
    \\ntf <message>
- Message must include at least one ping.
```'''}


def log(ctx, args):
    currentTime = time.localtime()
    logMessage = f'{time.strftime("%Y-%m-%d_%H.%M.%S", currentTime)} | {ctx.channel} | {ctx.author} used {ctx.command}: {" ".join(args)}'
    # logFile.write(f'\n{logMessage}')
    print(logMessage)


bot = commands.Bot(command_prefix='\\', help_command=None)


@bot.event
async def on_ready():
    currentTime = time.localtime()
    print(f'{bot.user} is connected!')
    # logFile.write(f'{time.strftime("%Y-%m-%d_%H.%M.%S", currentTime)} | {bot.user} is connected!')


@bot.command()
async def help(ctx, *args):
    if not args:
        await ctx.send(help_messages['standard'])
    else:
        await ctx.send(help_messages[args[0]])


@bot.command()
async def pingme(ctx, *args):
    await ctx.send(f'hi {ctx.author.mention}!')
    log(ctx, args)


@bot.command()
async def stop(ctx, *args):
    if ctx.author.id == MY_ID:
        await ctx.send('`shutting down...`')
        time.sleep(1)
        await ctx.send('`goodnight`')
        log(ctx, args)
        exit(code=0)


@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if user.bot:
        return
    if reaction.emoji == '✅' and message.id in ntf_messages:
        if user.id in ntf_messages[message.id]:
            ntf_messages[message.id].remove(user.id)
            if not ntf_messages[message.id]:
                await message.delete()


@bot.command()
async def bonk(ctx, mention, *args):
    if int(mention[3:-1]) != ctx.message.raw_mentions[0]:
        return
    try:
        times = int(args[0])
        args = args[1:]
    except:
        times = 1
    for n in range(0, times):
        await ctx.send(f'{mention} *bonk*')
    if args:
        await ctx.send(" ".join(args))
    else:
        await ctx.send(choice(bonkGifs))
        args = ' '
    log(ctx, args=[mention, str(times), " ".join(args)])


@bot.command()
async def say(ctx, *args):
    if ctx.author.id == MY_ID:
        await ctx.message.delete()
        await ctx.send('{}'.format(' '.join(args)))
        log(ctx, args)


@bot.command()
async def spampancake(ctx):
    pancake = await bot.fetch_user(517741581801881605)
    print(pancake)
    if ctx.author.id == MY_ID:
        for i in range(10):
            await pancake.send('https://discord.gg/euWDzqKD')
            print('message sent')

bot.run(TOKEN)
