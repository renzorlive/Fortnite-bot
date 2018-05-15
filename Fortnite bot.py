import discord
from discord.ext.commands import Bot
from discord.ext import commands
from pfaw import Fortnite, Platform
import random
import inspect
import sys
import os
import time

from analyzer import Analyzer


# CONSTANTS
botID = '443945180966682634' # bot ID on discord, used to prevent infinite topic loop
# responses for explicit !server or !status commands
serverStatusUpMessage = "Servers are UP"
serverStatusDownMessage = "Servers are DOWN"

# topic analysis: fortnite -> responses for server status up
fortniteServerStatusUp = ['fortnite is up', 'fortnite servers are up', "fortnite is up and running",
                          "servers are up", "servers up and running", "servers up",
                          "servers alive and kicking", "fortnite servers are good to go"]

# topic analysis: fortnite -> responses for server status down
fortniteServerStatusDown = ["fornite is down", "fortnite servers are up",
                                    "servers are down", "servers down", "servers are no go",
                                    "fortnite servers are down cold", "servers are sick with the flu"]
# end of sentences to make the responses more natural
endOfSentence = [', in case you were wondering', ', thought you might wanna know', ' btw',
                 ' for the record ', ' or so it seems', ', at least for now', ' atm',
                 ' at the moment', ' by the way']

# errors messages
errorSpecifyUsername = 'error: please specify an username'
errorNotFound = "error: user not found or servers are down, please try again"
errorInitializingFortnite = "an error has occured while trying to initialize Fortnite class"

decimalsShown = 3 # as in the statistics

# list of words related to the topic: fortnite
fortniteServerStatusRelatedWords = os.path.join(sys.path[0], "fortnite-servers-related.txt")
# list of words non-related to the topic: fortnite
fortniteServerStatusNonRelatedWords = os.path.join(sys.path[0], "fortnite-servers-non-related.txt")

# collect constants required for Fortnite class initialization from file settings.txt
with open("settings.txt", encoding="utf-8") as file:
    dataLines = [line.strip() for line in file]
fortniteToken = dataLines[0]
launcherToken = dataLines[1]
fortnitePassword = dataLines[2]
fortniteEmail = dataLines[3]
discordBotToken = dataLines[4]
# global initial initialization of fortnite class
try:
    fortnite = Fortnite(fortnite_token=fortniteToken,
                        launcher_token=launcherToken,
                        password=fortnitePassword, email=fortniteEmail)
except:
    print(errorInitializingFortnite)

# discord bot setup
Client = discord.Client()
client = commands.Bot(command_prefix = "`")

# amount of time in seconds between reinitializations of the fortnite class in order to refresh the token
tokenRefreshTime = 900 # TODO find the most efficient time

# GLOBAL VARIABLES
# keeps track of time since refresh
timeSinceLastRefresh = time.time()
timeOfMessage = time.time()


# on start...
@client.event
async def on_ready():
    print("Fortnite Bot is ready")


# on discord message event handler...
@client.event
async def on_message(message):
    # prepare required data
    userID = message.author.id # discord ID of whoever wrote the message
    words = message.content.split(" ") # list of words in discord message
    mentionPrefix = "<@" + userID + "> "
    
    # refresh token every tokenRefreshTime seconds
    global fortnite
    global timeOfMessage
    timeOfMessage = time.time()
    fortnite = refreshToken()
    
    #  fortnite kills command handler...
    if message.content.lower().startswith('!kills'):
        # if no parameters specified...
        if len(words) == 1:
            print(errorSpecifyUsername, 'line:', lineno()) # display error in console
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername) # inform author
            return # stop
    
        # determine mode and username
        args = getArgs(words) # arguments passed in the message
        # if no username was specified, display error
        if args == False:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        else:
            mode = args[0] # can be "no mode specified" if no mode was specified
            username = args[1]

        # get stats from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            print(errorNotFound, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorNotFound)
            return
        
        # if mode was specified... prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kills')
        # send response to discord
        await client.send_message(message.channel, responseMessage)
    
    
    # fortnite wins command handler...
    elif message.content.lower().startswith('!wins'):
        # if no parameters specified... error
        if len(words) == 1:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        
        # determine mode and username
        args = getArgs(words) # arguments passed in the message
        if args == False:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        else:
            mode = args[0]
            username = args[1]

        # try to get response from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            print(errorNotFound, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorNotFound)
            return

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'wins')
        # send response to discord
        await client.send_message(message.channel, responseMessage)

    # fortnite wins command handler...
    elif message.content.lower().startswith('!matches'):
        # if no parameters specified... error
        if len(words) == 1:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        
        # determine mode and username
        args = getArgs(words)
        if args == False:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        else:
            mode = args[0]
            username = args[1]

        # try to get response from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            print(errorNotFound, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorNotFound)
            return

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'matches')
        # send response to discord
        await client.send_message(message.channel, responseMessage)


    # fortnite winrate command handler...
    elif message.content.lower().startswith('!winrate'):
        # if no parameters specified... error
        if len(words) == 1:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        
        # determine mode and username
        args = getArgs(words)
        if args == False:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        else:
            mode = args[0]
            username = args[1]

        # try to get response from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            print(errorNotFound, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorNotFound)
            return

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'winrate')
        # send response to discord
        await client.send_message(message.channel, responseMessage)
        
    # fortnite kpm command handler...
    elif message.content.lower().startswith('!kpm'):
        # if no parameters specified... error
        if len(words) == 1:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        
        # determine mode and username
        args = getArgs(words)
        if args == False:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        else:
            mode = args[0]
            username = args[1]

        # try to get response from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            print(errorNotFound, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorNotFound)
            return

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kpm')
        # send response to discord
        await client.send_message(message.channel, responseMessage)

    # fortnite kpd command handler...
    elif message.content.lower().startswith('!kpd'):
        # if no parameters specified... error
        if len(words) == 1:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        
        # determine mode and username
        args = getArgs(words)
        if args == False:
            print(errorSpecifyUsername, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorSpecifyUsername)
            return
        else:
            mode = args[0]
            username = args[1]

        # try to get response from Fortnite API for username
        try:
            stats = fortnite.battle_royale_stats(username=username, platform=Platform.pc)
        except:
            print(errorNotFound, 'line:', lineno())
            await client.send_message(message.channel, mentionPrefix + errorNotFound)
            return

        # prepare response message
        responseMessage = getCommandResponse(mode, stats, message, userID, username, 'kpd')
        # send response to discord
        await client.send_message(message.channel, responseMessage)

    # fortnite server status command handler...
    elif (message.content.lower().startswith('!server') or message.content.startswith('!servers')
    or message.content.startswith('!status')):
        status = fortnite.server_status()
        if status:
            await client.send_message(message.channel, mentionPrefix + serverStatusUpMessage)
        else:
            await client.send_message(message.channel, mentionPrefix + serverStatusDownMessage)
    
    # natural language topic analyses (non explicit commands, analyzing normal converstion)
    # analyze topic, if it's about fortnite, respond with server status in a somewhat natural way
    elif(isTopicFortnite(message, mentionPrefix)):
        status = fortnite.server_status()
        if status:
            await client.send_message(message.channel, (mentionPrefix+
                                                        random.choice(fortniteServerStatusUp)+
                                                        random.choice(endOfSentence)))
        else:
            await client.send_message(message.channel, (mentionPrefix+
                                                        random.choice(fortniteServerStatusDown)+
                                                        random.choice(endOfSentence)))



# natural language analyzers
def isTopicFortnite(message, mentionPrefix):
    """
    message: object; mentionPrefix: string
    returns bool
    Analyzes sentence and returns true if topic is about fortnite, false otherwise
    """
    # if message is from bot, ignore
    if message.author.id == botID:
        return False
    
    # initialize analyzer
    analyzer = Analyzer(fortniteServerStatusRelatedWords, fortniteServerStatusNonRelatedWords)
    if not analyzer:
        print('error trying to initialize Analyzer', 'line:', lineno())
        client.send_message(message.channel, mentionPrefix + ' error while trying to initialize Analyzer line: ' + str(lineno()))
        return False
    
    score = analyzer.analyze(message.content)
    return score >= 2



# helpers
def refreshToken():
    global timeSinceLastRefresh
    global timeOfMessage
    global fortnite
    # change in time since the last refresh until now
    dt = timeOfMessage - timeSinceLastRefresh
    # if defined time between refreshes is exceeeded, refresh token and reset time
    if dt >= tokenRefreshTime:
        timeSinceLastRefresh = timeOfMessage
        return initializeFortnite()
    return fortnite


def initializeFortnite():
    # initialize the Fortnite class, if it already exists, it refreshes the token
    fortnite = Fortnite(fortnite_token=fortniteToken,
                                launcher_token=launcherToken,
                                password=fortnitePassword, email=fortniteEmail)
    return fortnite

    
def getArgs(words):
    mode = 'no mode specified' # initial assumption
    # determine specified parameters
    if isMode(words[1]):
        if len(words) == 2:
            print('no username provided', 'line:', lineno())
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


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


def getCommandResponse(mode, stats, message, userID, username, stat):
    """handler for static commands"""
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
            datasquad = stats.squad.wins / stats.squad.matches * 100
        elif stat == 'kpm':
            dataall = stats.all.kills / stats.all.matches
            datasolo = stats.solo.kills / stats.solo.matches
            dataduo = stats.duo.kills / stats.duo.matches
            datasquad = stats.squad.kills / stats.squad.matches
        elif stat == 'kpd':
            dataall = stats.all.kills / (stats.all.matches - stats.all.wins)
            datasolo = stats.solo.kills / (stats.solo.matches - stats.solo.wins)
            dataduo = stats.duo.kills / (stats.duo.matches - stats.duo.wins)
            datasquad = stats.squad.kills / (stats.squad.matches - stats.squad.wins)
            
        # prepare response for when mode is not specified
        responseMessage = ("<@"+userID+"> "+username+": "+
                           str(round(dataall, decimalsShown))+" all "+stat+"; "+
                           str(round(datasolo, decimalsShown))+" solo "+stat+"; "+ 
                           str(round(dataduo, decimalsShown))+" duo "+stat+"; "+
                           str(round(datasquad, decimalsShown))+" squad "+stat)
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
        elif stat == 'kpd':
            data = stats.all.kills / (stats.all.matches - stats.all.wins);
            
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
        elif stat == 'kpd':
            data = stats.solo.kills / (stats.solo.matches - stats.solo.wins);
    
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
        elif stat == 'kpd':
            data = stats.duo.kills / (stats.duo.matches - stats.duo.wins);
    
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
        elif stat == 'kpd':
            data = stats.squad.kills / (stats.squad.matches - stats.squad.wins);    
        
    # prepare response message for when mode is specified
    responseMessage =  ("<@"+userID+"> "+username+": "+
                        str(round(data, decimalsShown))+" "+mode+" "+stat)
    return responseMessage



client.run(discordBotToken)