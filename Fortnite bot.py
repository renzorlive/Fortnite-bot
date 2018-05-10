import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from pfaw import Fortnite, Platform


# collect required data from file settings.txt
with open("settings.txt", encoding="utf-8") as file:
    dataLines = [line.strip() for line in file]
# prepare required data for setup
fortniteToken = dataLines[0]
launcherToken = dataLines[1]
fortnitePassword = dataLines[2]
fortniteEmail = dataLines[3]
discordBotToken = dataLines[4]

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
    words = message.content.split(" ") # list of words in discord message
    
    #  fortnite kills command...
    if message.content.startswith('!kills'):
        # if no parameters specified... error
        if len(words) == 1:
            await client.send_message(message.channel, 'error: please specify at least an username')
            return
        
        args = getArgs(words)
        if args == False:
            await client.send_message(message.channel, 'error: please specify an username')
            return
        else:
            mode = args[0]
            username = args[1]

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
            responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kills')
            # send response to discord
            await client.send_message(message.channel, responseMessage)
            return # stop
        
        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kills')
        # send response to discord
        await client.send_message(message.channel, responseMessage)
    
    # fortnite wins command...
    elif message.content.startswith('!wins'):
        # if no parameters specified... error
        if len(words) == 1:
            await client.send_message(message.channel, 'error: please specify at least an username')
            return
        
        args = getArgs(words)
        if args == False:
            await client.send_message(message.channel, 'error: please specify an username')
            return
        else:
            mode = args[0]
            username = args[1]

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
            responseMessage = getCommandResponse(mode, stats, message, userID, username, 'wins')
            # send response to discord
            await client.send_message(message.channel, responseMessage)
            return # stop

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'wins')
        # send response to discord
        await client.send_message(message.channel, responseMessage)

    # fortnite wins command...
    elif message.content.startswith('!matches'):
        # if no parameters specified... error
        if len(words) == 1:
            await client.send_message(message.channel, 'error: please specify at least an username')
            return
        
        args = getArgs(words)
        if args == False:
            await client.send_message(message.channel, 'error: please specify an username')
            return
        else:
            mode = args[0]
            username = args[1]

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
            responseMessage = getCommandResponse(mode, stats, message, userID, username, 'matches')
            # send response to discord
            await client.send_message(message.channel, responseMessage)
            return # stop

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'matches')
        # send response to discord
        await client.send_message(message.channel, responseMessage)


    # fortnite winrate command...
    elif message.content.startswith('!winrate'):
        # if no parameters specified... error
        if len(words) == 1:
            await client.send_message(message.channel, 'error: please specify at least an username')
            return
        
        args = getArgs(words)
        if args == False:
            await client.send_message(message.channel, 'error: please specify an username')
            return
        else:
            mode = args[0]
            username = args[1]

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
            responseMessage = getCommandResponse(mode, stats, message, userID, username, 'winrate')
            # send response to discord
            await client.send_message(message.channel, responseMessage)
            return # stop

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'winrate')
        # send response to discord
        await client.send_message(message.channel, responseMessage)
        
        
    # fortnite kpm command...
    elif message.content.startswith('!kpm'):
        # if no parameters specified... error
        if len(words) == 1:
            await client.send_message(message.channel, 'error: please specify at least an username')
            return
        
        args = getArgs(words)
        if args == False:
            await client.send_message(message.channel, 'error: please specify an username')
            return
        else:
            mode = args[0]
            username = args[1]

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
            responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kpm')
            # send response to discord
            await client.send_message(message.channel, responseMessage)
            return # stop

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kpm')
        # send response to discord
        await client.send_message(message.channel, responseMessage)



# helpers        
def getCommandResponse(mode, stats, message, userID, username, stat):
    # if no mode was specified, showing data for all modes...
    if mode == 'no mode specified':
        # prepare data
        if stat == 'kills':
            dataall = stats.all.kills
            datasolo = stats.solo.kills
            dataduo = stats.duo.kills
            datasquad = stats.squad.kills
        elif stat == 'wins':
            dataall = stats.all.wins
            datasolo = stats.solo.wins
            dataduo = stats.duo.wins
            datasquad = stats.squad.wins
        elif stat == 'matches':
            dataall = stats.all.matches
            datasolo = stats.solo.matches
            dataduo = stats.duo.matches
            datasquad = stats.squad.matches
        elif stat == 'winrate':
            dataall = stats.all.wins / stats.all.matches * 100
            datasolo = stats.solo.wins / stats.solo.matches * 100
            dataduo = stats.duo.wins / stats.duo.matches * 100
            datasquad = stats.squad.wins / stats.squad * 100
        elif stat == 'kpm':
            dataall = stats.all.kills / stats.all.matches
            datasolo = stats.solo.kills / stats.solo.matches
            dataduo = stats.duo.kills / stats.duo.matches
            datasquad = stats.squad.kills / stats.squad.matches
            
        # prepare response
        responseMessage = ("<@"+userID+"> "+username+": "+str(dataall)+" all kills; "+
                          str(datasolo)+" solo kills; "+ str(dataduo)+" duo kills; "+
                          str(datasquad)+" squad kills")
        return responseMessage
    
    # if mode was specified, prepare the appropriate data
    if mode == 'all':
        if stat == 'kills':
            data = stats.all.kills
        elif stat == 'wins':
            data = stats.all.wins
        elif stat == 'matches':
            data = stats.all.matches
        elif stat == 'winrate':
            data = stats.all.wins / stats.all.matches * 100
        elif stat == 'kpm':
            data = stats.all.kills / stats.all.matches
            
    elif mode == "solo":
        if stat == 'kills':
            data = stats.solo.kills
        elif stat == 'wins':
            data = stats.solo.wins
        elif stat == 'matches':
            data = stats.solo.matches
        elif stat == 'winrate':
            data = stats.solo.wins / stats.solo.matches * 100
        elif stat == 'kpm':
            data = stats.solo.kills / stats.solo.matches
  
    elif mode == 'duo':
        if stat == 'kills':
            data = stats.duo.kills
        elif stat == 'wins':
            data = stats.duo.wins
        elif stat == 'matches':
            data = stats.duo.matches
        elif stat == 'winrate':
            data = stats.duo.wins / stats.all.matches * 100
        elif stat == 'kpm':
            data = stats.duo.kills / stats.all.matches
    
    elif mode == 'squad':
        if stat == 'kills':
            data = stats.squad.kills
        elif stat == 'wins':
            data = stats.squad.wins
        elif stat == 'matches':
            data = stats.squad.matches
        elif stat == 'winrate':
            data = stats.squad.wins / stats.squad.matches * 100
        elif stat == 'kpm':
            data = stats.squad.kills / stats.squad.matches
            
    # prepare response message
    responseMessage =  "<@" + userID + "> " + username + ": " + str(data) + " " + mode + " kills"
    return responseMessage

def getArgs(words):
    mode = 'no mode specified' # initial assumption
        # determine specified parameters
    if isMode(words[1]):
        if len(words) == 2:
            print('no username provided') # TODO
            return False
        mode = words[1]
        username = words[2]
    else:
        username = words[1]
        if len(words) >= 3 and isMode(words[2]):
            mode = words[2]
    return [mode, username]
    
def isMode(word):
    return (word == 'all' or word == 'solo' or word == 'duo' or word == 'squad')

client.run(discordBotToken)