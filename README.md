# Fortnite-bot

**Invite the bot: https://discordapp.com/api/oauth2/authorize?client_id=443945180966682634&permissions=8&scope=bot**

Donations: https://www.paypal.me/fsil

# Available commands:
**!kills mode username** (mode is one of: all, solo, duo or squads; username: your fortnite username)

**!kills username mode** (alternative way)

**!kills username** (by ommiting the mode, bot shows data from all modes for username)

**same pattern as above works for: kills, wins, matches, winrate, kpm**

**!server; !servers; !status (displays the status of fortnite servers)**

**The bot has natural language analysis capabilities, right now limited but in development; e.g. "hey Mike, do you wanna play fortnite ?"; The bot will then respond with the servers status e.g. "servers are up by the way"**

# IMPORTANT: Your conversations or data are not collected in any way.

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
- Added demimal rounding to 3 decimals to bot responses
- Updated error logging

**13-may-18**
- Fixed token timeout issue, bot will now work indefinetly
- Added natural language analysis
- Cleaned up code, removed redudant commands, now relying on natural language alanysis (but not all commands removed yet)
- Cleaned up code, improved natural language analysis
- Improved natural language scoring