# Fortnite-bot

**Invite the bot: https://discordapp.com/api/oauth2/authorize?client_id=443945180966682634&permissions=8&scope=bot**

Donations: https://www.paypal.me/fsil

# Available commands:
**!kills mode username** (mode is one of: all, solo, duo or squads; username: your fortnite username)

**!kills username mode** (alternative way)

**!kills username** (by ommiting the mode, bot shows data from all modes for username)

**same pattern as above works for: kills, wins, matches, winrate, kpm**

**!server; !servers; !status (displays the status of fortnite servers)**

**you can ask the bot about the servers status as so: is fortnite up ?; are fortnite servers up ?; fortnite up ?; are servers up ?; not case sensitive**


# Changelog 
**10-may-18**
- Added error handling for data retrieval, the bot will now notify you if errors occur.
- Added settings.txt to store critical data outside the code
- Added flexible command, can now ommit the mode
- Added more error handling
- Added more flexibility to commands logic
- Simplified code readability
- Added the rest of the stats commands, kills, wins, matches, winrate, kpm; improved code logic and readability
- Added server status commands, added some natural interaction with bot, you can now ask about the servers status
- Added mentions to bot response
- Improved code readability; updated error messages
- Fixed bot responses for given stat; e.g. !wins username would return username: someNumber mode kills; ...