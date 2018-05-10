import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from pfaw import Fortnite, Platform


# collect data from file settings.txt
with open("settings.txt", encoding="utf-8") as file:
    dataLines = [line.strip() for line in file]
# prepare required data for setup
fortniteToken = dataLines[0]
launcherToken = dataLines[1]
fortnitePassword = dataLines[2]
fortniteEmail = dataLines[3]
discordBotToken = dataLines[4]


# TODO check if stats update, otherwise delete this and use the function getFortniteData instead
try:
    fortnite = Fortnite(fortnite_token=fortniteToken,
                        launcher_token=launcherToken,
                        password=fortnitePassword, email=fortniteEmail)
except:
    print("an error has occured while trying to initialize Fortnite class")


# discord bot setup
Client = discord.Client()
client = commands.Bot(command_prefix = "`")

@client.event
async def on_ready():
    print("Fortnite Bot is ready")


@client.event
async def on_message(message):
    userID = message.author.id
    words = message.content.split(" ") # list of words in message
    
    # fortnite kills command
    if message.content.startswith('!kills'):
        mode = words[1]
        username = words[2]

        # try to get response from Fortnite API
        try:
            # TODO counting the time until stats are retrieved for debugging purpuses
            t1 = time.time() 
            #fortnite = getFortniteData(); # TOO check if stats update, otherwise use the function
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
            dt = time.time() - t1 # TODO debugging delta time before and after the stats retrieval
        except:
            errorMsg = "error: user not found or servers are down, please try again"
            print(errorMsg)
            await client.send_message(message.channel, errorMsg)
            return
        
        # prepare appropriate data
        if mode == 'all':
            kills = stats.all.kills
        elif mode == "solo":
            kills = stats.solo.kills
        elif mode == 'duo':
            kills = stats.duo.kills
        elif mode == 'squad':
            kills = stats.squad.kills
        
        # prepare response message
        responseMessage =  "<@" + userID + "> " + username + ": " + str(kills) + " kills in " + mode
        
        # send message to discord
        await client.send_message(message.channel, responseMessage)
        
        # TODO sending the time for debugging
        await client.send_message(message.channel, "debug: request compleated in " + str(dt) + " s") 


# helpers

# NOT USED
# TODO check if stats update, if not, use this function to get data every time it's needed
def getFortniteData():
    fortnite = Fortnite(fortnite_token=fortniteToken,
                        launcher_token=launcherToken,
                        password=fortnitePassword, email=fortniteEmail)
    return fortnite



client.run(discordBotToken)