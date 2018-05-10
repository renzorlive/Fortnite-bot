import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from pfaw import Fortnite, Platform

# fortnite example variables
#stats = fortnite.battle_royale_stats(username='silver_0_wins', platform=Platform.pc)
#kpm = stats.solo.kills / stats.solo.matches

# TODO check if stats update, otherwise delete this and use the function getFortniteData instead
fortnite = Fortnite(fortnite_token='ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=',
                launcher_token='MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=',
                password='SILVER@kerokero955', email='silvermirai@yahoo.com')

# discord bot setup
Client = discord.Client()
client = commands.Bot(command_prefix = "`")

@client.event
async def on_ready():
    print("Fortnite Bot is ready")


@client.event
async def on_message(message):
    if message.content.startswith('!kills'):
        userID = message.author.id
        words = message.content.split(" ") # list of words in message
        mode = words[1]
        username = words[2]

        # try to get response from Fortnite API
        try:
            # TODO counting the time until stats are retrieved for debugging purpuses
            t1 = time.time() 
            #fortnite = getFortniteData(); # TOO check if stats update, otherwise use the function
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
            dt = time.time() - t1 # TODO debugging delta time before and after the stats retrieval
        except ValueError:
            await client.send_message(message.channel, "error: user not found or servers are down")
            return
            
        if mode == "solo":
            kills = stats.solo.kills
        else:
            kills = "placeholder TODO"
        
        responseMessage =  "<@" + userID + "> " + username + ": " + str(kills) + " kills in solo"
        
        await client.send_message(message.channel, responseMessage)
        
        # TODO sending the time for debugging
        await client.send_message(message.channel, str(dt) + "s") 



# helpers
# TODO check if stats update, if not, use this function to get data every time it's needed
def getFortniteData():
    fortnite = Fortnite(fortnite_token='ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=',
                launcher_token='MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=',
                password='SILVER@kerokero955', email='silvermirai@yahoo.com')
    return fortnite



client.run("NDQzOTQ1MTgwOTY2NjgyNjM0.DdUxDw.REPTZrzUAvmjhex7x9xHKrBXd-E")