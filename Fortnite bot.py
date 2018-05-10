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
        # if no parameters specified... error
        if len(words) == 1:
            await client.send_message(message.channel, 'error: please specify at least an username')
            return
        
        mode = 'no mode specified' # initial assumption
        # determine specified parameters
        if isMode(words[1]):
            print('isword') # TODO
            if len(words) == 2:
                print('no username provided') # TODO
                await client.send_message(message.channel, 'error: please specify an username')
                return
            mode = words[1]
            username = words[2]
        else:
            username = words[1]

        # try to get response from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            errorMsg = "error: user not found or servers are down, please try again"
            print(errorMsg)
            await client.send_message(message.channel, errorMsg)
            return
        
        # if no mode was specified, showing data for all modes...
        if mode == 'no mode specified':
            # prepare data
            killsall = stats.all.kills
            killssolo = stats.solo.kills
            killsduo = stats.duo.kills
            killssquad = stats.squad.kills
            # prepare response
            responseMessage = ("<@"+userID+"> "+username+": "+str(killsall)+" all kills; "+
                              str(killssolo)+" solo kills; "+ str(killsduo)+" duo kills; "+
                              str(killssquad)+" squad kills")
            # send response to discord
            await client.send_message(message.channel, responseMessage)
            return # stop
        
        
        # if mode was specified, prepare the appropriate data
        if mode == 'all':
            kills = stats.all.kills
        elif mode == "solo":
            kills = stats.solo.kills
        elif mode == 'duo':
            kills = stats.duo.kills
        elif mode == 'squad':
            kills = stats.squad.kills
        # prepare response message
        responseMessage =  "<@" + userID + "> " + username + ": " + str(kills) + " " + mode + " kills"
        # send response to discord
        await client.send_message(message.channel, responseMessage)


# helpers
def isMode(word):
    return (word == 'all' or word == 'solo' or word == 'duo' or word == 'squad')

client.run(discordBotToken)