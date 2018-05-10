import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from pfaw import Fortnite, Platform

# fortnite api setup
fortnite = Fortnite(fortnite_token='ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=',
                launcher_token='MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=',
                password='SILVER@kerokero955', email='silvermirai@yahoo.com')

# fortnite example variables
#stats = fortnite.battle_royale_stats(username='silver_0_wins', platform=Platform.pc)
#kpm = stats.solo.kills / stats.solo.matches


# discord bot setup
Client = discord.Client()
client = commands.Bot(command_prefix = "`")

@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_message(message):
    if message.content.startswith('!kills'):
        userID = message.author.id
        words = message.content.split(" ") # list of words in message
        mode = words[1]
        username = words[2]

        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except ValueError:
            await client.send_message(message.channel, "error: user not found or servers are down")
            return
            
        if mode == "solo":
            kills = stats.solo.kills
        else:
            kills = "placeholder TODO"
        
        responseMessage =  "<@" + userID + "> " + username + ": " + str(kills) + " kills in solo"
        
        await client.send_message(message.channel, responseMessage)





client.run("NDQzOTQ1MTgwOTY2NjgyNjM0.DdUxDw.REPTZrzUAvmjhex7x9xHKrBXd-E")