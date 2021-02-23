import discord
import os
from discord.ext import commands
from binance.client import Client
from discord.ext.commands import bot

## api einbindungen
binance_api =  os.environ.get('binance_api')
binance_secret = os.environ.get('binance_secret')
discord_api = os.environ.get('discord_api')

binance_client = Client(binance_api, binance_secret)
bot_client = commands.Bot(command_prefix = '$')

command_list = ['ping', 'test', 'doge', 'doge amount', 'dogeF', 'dogef', 'help']

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
@bot_client.command()
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
@bot_client.command(aliases = ['dogef'])
async def dogeF(ctx):
    amount = float(binance_client.get_asset_balance(asset='Doge')['free'])
    doge_price = float(binance_client.get_symbol_ticker(symbol="DOGEEUR")['price'])
    await ctx.send(f'{round(amount*doge_price,2)}€ in Freddys Depot')
    
    
# test command
@bot_client.command()
async def hi(ctx):
    await ctx.send('Hello')
    
    
# gibt die Primfaktoren einer Zahl zurück
@bot_client.command()
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
        await ctx.send('Ne, also solche Zahlen kann ich nicht faktorisieren. \n Bitte gib eine Zahl, welche kleiner ist als  ein!')
        return
    
    factors = []
    
    f=2
    while f<=number:
        if number%f==0:
            factors.append(f)
            number=number/f
        else:
            f+=1
            
    await ctx.send(factors)
    
bot_client.run(discord_api)
