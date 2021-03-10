import discord
import os
import random
import requests

from discord.ext import commands
from binance.client import Client
from discord.ext.commands import bot
from bs4 import BeautifulSoup
from math import sqrt

## api einbindungen
binance_api =  os.environ.get('binance_api')
binance_secret = os.environ.get('binance_secret')
discord_api = os.environ.get('discord_api')

binance_client = Client(binance_api, binance_secret)

## prefix ist $
bot_client = commands.Bot(command_prefix = '$')



## sobald der bot online ist
@bot_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot_client))
    

## commands für den bot

# Ping test
@bot_client.command(aliases = ['test'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot_client.latency * 1000)}ms')


# gebe den aktuellen dogecoin kurs aus, inkl. mengenangabe
@bot_client.command(name='doge',help='gibt den Preis von 1 oder mehreren Dogecoins an')
async def doge(ctx, amount=1.0):
    
    if amount <= 0:
        await ctx.send('seriously? Du musst schon eone Zahl größer als 0 angeben.')
        return
    
    doge_price = binance_client.get_symbol_ticker(symbol="DOGEEUR")['price']
    # runde auf 4 Nachkommastellen
    doge_price = round(float(doge_price), 4) 
    
    if amount == 1:
        await ctx.send(f'{doge_price}€')
        return
    else:
        await ctx.send(f'{round(amount*doge_price,2)}€')


# gebe den aktuellen wert von freddy dogecoin an
@bot_client.command(name='dogeF', aliases = ['dogef'], help='Freddys Dogecoin Depot')
async def dogeF(ctx):
    amount = float(binance_client.get_asset_balance(asset='Doge')['free'])
    doge_price = float(binance_client.get_symbol_ticker(symbol="DOGEEUR")['price'])
    await ctx.send(f'{round(amount*doge_price,2)}€ in Freddys Depot')
    
    
# test command
@bot_client.command()
async def hi(ctx):
    await ctx.send('Hello')
    
# gibt die Primfaktoren einer Zahl zurück
@bot_client.command(name='factorize',help='zerlegt eine zahl in ihre primfaktoren')
async def factorize(ctx, number):
    
    try:
        number = int(number)
    except:
        await ctx.send('Wie soll ich das denn faktorisieren?')
        return
        
    if number == 1:
        await ctx.send('Was ein funny boy bist du denn?')
        return
    if number <= 0:
        await ctx.send('Ne, also solche Zahlen kann ich nicht faktorisieren. \nBitte gib eine Zahl, welche größer ist als 1, ein!')
        return
    
    factors = []
    
    f=2
    while f<=number:
        if number%f==0:
            factors.append(f)
            number=number/f
        else:
            f+=1
    
    if len(factors) == 1:
        await ctx.send('Herzlichen Glückwunsch, du hast eine Primzahl gefunden!')
    await ctx.send(factors)


# falschen bot zum musik spielen gewählt?
@bot_client.command()
async def play(ctx, arg):
    await ctx.send(f'Meintest du "!play {arg}" ?')
    
    
# öffne wikipedia mit bestimmten keyword
@bot_client.command(name='wiki',help='öffnet wikipedia')
async def wiki(ctx, *keyword):
    if keyword == 'paul' or keyword == 'discordbot':
        await ctx.send('Du hast ein Easter-Egg gefunden!')
    
    suchbegriff = ""
    for word in keyword:
        suchbegriff += word
        suchbegriff += '_'
        
    link = f'https://de.wikipedia.org/wiki/{suchbegriff}'
    await ctx.send(link)
    

# für menschen, die an paul mitarbeiten wollen
@bot_client.command(name='contribute', help='Wenn man an Paul mitarbeiten möchte')
async def contribute(ctx):
    link = r'https://github.com/FeudalFreddy/discord-paul'
    await ctx.send(f'Du möchstest an Paul mitarbeiten? \nUnter diesem Link findest du meinen Sourcecode:\n{link}')


# random number generator
@bot_client.command(aliases = ['randomnumber', 'random', 'numbergenerator'], name='rng', help='Gibt eine Zufallszahl aus')
async def rng(ctx, lower=1, upper=100):
    await ctx.send(f'Zufallszahl zwischen {lower} und {upper}? Kommt sofort!')
    await ctx.send(random.randint(lower,upper))


# minecraft crafting rezepte
@bot_client.command(name='craft', help='Gibt (evtl.) ein Craftingrezept für ein bestimmtes Item an')
async def craft(ctx, recipe):
                
    link_article = 'https://www.minecraftcrafting.info/'
    link_pic = f'view-source:https://www.minecraftcrafting.info/imgs/craft_{recipe}.png'
    await ctx.send(link_pic)
    await ctx.send('Falls du hier kein Craftingrezept siehst, liegt dass daran dass du den Block falsch geschrieben hast.')


# löscht alle nachrichten in einem beliebigen Channel
@bot_client.command(name = 'purge', help ='Löscht alle Nachrichten in einem Chat, wenn man die Rechte hat')
async def purge(ctx):
    if str(ctx.author) == os.environ.get('admin_user'):
        await ctx.channel.purge()
    else:
        await ctx.send('Du hast leider nicht die Rechte für diesen Befehl')

# gibt die Nullstellen einer quadratischen Gleichung an
@bot_client.command(name='xSolve', help='gibt die Nullstellen einer quadratischen Gleichung an')
async def xSolve(ctx, a=0, b=0, c=0):
    if a == 0 and b == 0 and c == 0:
        await ctx.send('Du musst Parameter angeben')
        return
    
    try:
        x1 = round((-b+sqrt(b*b-4*a*c))/(2*a),4)
        x2 = round((-b-sqrt(b*b-4*a*c))/(2*a),4)
    except:
        await ctx.send(f'Leider hat deine Funktion keine Nullstellen')
        return
    
    await ctx.send(f'Deine Lösungen sind x1= {x1} und x2= {x2}')
    
    
bot_client.run(discord_api)
