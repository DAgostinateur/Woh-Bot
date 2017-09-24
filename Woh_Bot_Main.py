import discord
from datetime import datetime
from datetime import date
import asyncio
import subprocess
import os
import sys
from tabulate import tabulate #https://pypi.python.org/pypi/tabulate
from util import *
from hidden import * # Things that I don't want to have seen by the public
                     # I'm the only one with access to this

#TODO LIST :
# - More user friendly removal of birthdays
# - Setting the BD channel with a command
# - Server checker, preventing the bot from sending a message to the wrong server
# - List of users that has access to BD commands
# - Level of access to commands
# - Updates m_EmojiList, m_MemberList, m_ChannelList when added, removed or updated

Prefix = '!' # The prefix that will be used for commands
client = discord.Client()
m_EmojiList = []
m_MemberList = []
m_ChannelList = []
m_UserBDList = []
m_ChannelBDList = []
HelpMessage = """**My prefix is [{0}].
Here's my list of commands:**
- {0}city [someone] -> Population of the city
- {0}town [someone] -> Population of the town
- {0}addBD [@user] [mm-dd] -> Adds a user to my birthday list
- {0}removeBD [@user] [mm-dd] -> Removes a user from my birthday list
- {0}listBD -> Lists everyone from my birthday list""".format(Prefix)


def ExtractInfo():
    for server in client.servers:
        server = discord.Channel(server)
        for member in server.members:   # Collects every Member from every server
            m_MemberList.append(member) # Repeats Members if they are in multiple servers with the bot
        for emoji in server.emojis:     # Collects every Emoji from every server
            m_EmojiList.append(emoji)
        for channel in server.channels: # Collects every Channel from every server
            m_ChannelList.append(channel)
    FileExtractUserBD(m_UserBDList)     # Collects every UserBd from FileNameUserBD()
    print("List of Members has been extracted.")
    print("List of Emojis has been extracted.")
    print("List of Channels has been extracted.")
    print("List of UserBD has been extracted.") 

def HappyBirthdayMessage(p_mm_dd : str):
    BdMessage = ""
    HappyB = "{} Happy Birthday ".format(ObtainEmojiWithName(m_EmojiList, "woh"))
    userBdToday = []

    for userBd in m_UserBDList:
        if p_mm_dd == userBd.bd: # We're checking for people's birthdays and adding them to userBdToday[]
            userBdToday.append(userBd)

    if len(userBdToday) != 0: # We're checking if there's anyone in userBdToday[]
        for nbUser in userBdToday:
            BdMessage = BdMessage + HappyB + nbUser.userId + "\n\n"
        return BdMessage
    else:
        return ""

async def HappyBirthdayTimer():
    await client.wait_until_ready()
    while not client.is_closed:
        mm_dd = str(date.today())[5:]
        text = HappyBirthdayMessage(mm_dd)
        if text != "":
            await client.send_message(discord.Object(id='293438398050598912'), text) # The channelID is #discussion

        today_n = datetime.today()
        today_t = today_n.replace(day=today_n.day + 1, hour=11, minute=0, second=0, microsecond=0)
        delta_secs = int((today_t - today_n).seconds + 1)
        print(today_n)
        await asyncio.sleep(delta_secs) # Task runs every day at 11am


@client.event
async def on_ready():
    ExtractInfo()
    print("---------\nWoh Bot\n---------")
    print("Logged in as " + str(client.user))
    print("Creator : D'Agostinateur Woh")
    print("---------")


@client.event
async def on_reaction_add(reaction, user):
    if False: # Only here to help me, it actually breaks the bot
        reaction = discord.Reaction()
        user = discord.User()

    if user != client.user: # Idk if it would cause an infinite loop without this
        if reaction.emoji == ObtainEmojiWithName(m_EmojiList, "woh"):
             await client.add_reaction(reaction.message, ObtainEmojiWithName(m_EmojiList, "woh"))


@client.event
async def on_message(message):
    if False: # Only here to help me, it actually breaks the bot
        message = discord.Message(message)

    if message.author != client.user: # This prevents the bot from responding to itself
        #HELP_START
        if message.content.startswith(Prefix + "help"):
            await client.send_message(message.author, HelpMessage)
            await client.delete_message(message)
            if message.author.id == MyID():
                extraHelp = "**You are allowed see and use these special commands.**\n- {0}openTV -> Opens TeamViewer\n- {0}closeTV -> Closes TeamViewer ".format(Prefix)
                await client.send_message(message.author, extraHelp)
        #HELP_END

        #WOH REACTION_START
        if "woh" in message.content.lower():
            await client.add_reaction(message, ObtainEmojiWithName(m_EmojiList, "woh"))
        #WOH REACTION_END

        #OPEN TEAMVIEWER_START
        if message.content.startswith(Prefix + "openTV"):
            if message.author.id == MyID:
                await client.send_message(message.channel, "Opening TeamViewer...")
                subprocess.call(CmdOpenTV()) # Opens TeamViewer.exe
            else:
                await client.send_message(message.channel, "**You do not have access to this command**")
        #OPEN TEAMVIEWER_END
        #CLOSE TEAMVIEWER_START
        if message.content.startswith(Prefix + "closeTV"):
            if message.author.id == MyID():
                await client.send_message(message.channel, "Closing TeamViewer...")
                os.system(CmdCloseTV()) # Closes TeamViewer.exe
            else:
                await client.send_message(message.channel, "**You do not have access to this command**")
        #CLOSE TEAMVIEWER_END

        #TOWN_START
        if message.content.startswith(Prefix + "town"):
            command = str(message.content)[6:] # Removes the "!town " from the content
            if len(command) != 0:
                msg = "Shut the Fuck Up Town\nPopulation: {}".format(command)
                await client.send_message(message.channel, msg)
                await client.delete_message(message)
        #TOWN_END
        #CITY_START
        if message.content.startswith(Prefix + "city"):
            command = str(message.content)[6:] # Removes the "!city " from the content
            if len(command) != 0:
                msg = "Gotem City\nPopulation: {}".format(command)
                await client.send_message(message.channel, msg)
                await client.delete_message(message)
        #CITY_END

        #BIRTHDAY CHANNEL DISPLAY_START
        if message.content.startswith(Prefix + "showChannelBD"):
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == str(message.server.id):
                    await client.send_message(message.channel, "I send birthday messages to {}.".format(channelBD.channelId))
                    return
            await client.send_message(message.channel, "I don't send birthday messages in this server.")
        #BIRTHDAY CHANNEL DISPLAY_END
        #BIRTHDAY CHANNEL ADDER_START    
        if message.content.startswith(Prefix + "addChannelBD"):
            command = str(message.content)[14:] # Removes the "!addChannelBD " from the content
            channelId = str(command)
            serverId = str(message.server.id)
            if not IsChannelIdValid(m_ChannelList, channelId):
                await client.send_message(message.channel, "**Invalid channel**, make sure you entered a real channel from this server.")
                return
            
            for channelBD in m_ChannelBDList:
                if channelBD.channelId == channelId:
                    await client.send_message(message.channel, "**There's already a channel for birthday messages in this server**, delete the current one to change it.")
                    return

            await client.send_message(message.channel, "I will now send birthday messages in {}.".format(channelId)) # If this sends a message, it means everything is valid
            FileAddChannelBD(m_ChannelBDList, channelId, serverId)
        #BIRTHDAY CHANNEL ADDER_END
        #BIRTHDAY CHANNEL REMOVED_START
        if message.content.startswith(Prefix + "removeChannelBD"):
            serverId = str(message.server.id)
            listIndex = 0 # We're sending the index to FileRemoveUserBD
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == serverId:
                    FileRemoveChannelBD(m_ChannelBDList, listIndex)
                    await client.send_message(message.channel, "I will no longer send birthday messages in this server.")
                    return
                listIndex += 1
            await client.send_message(message.channel, "There's no channel to remove.")
        #BIRTHDAY CHANNEL REMOVED_END

        #LIST BIRTH DATES_START
        if message.content.startswith(Prefix + "listBD"):
            if len(m_UserBDList) != 0:
                comboList = []
                for userBd in m_UserBDList:
                    name = ObtainMemberInfo(m_MemberList, userBd.ObtainPureUserID(), "na")
                    comboList.append([name, userBd.bd])
                    if len(comboList) == 10:
                        fullMessage = "```" + tabulate(comboList, headers=["Name", "Birthday"], tablefmt="fancy_grid") + "```"
                        await client.send_message(message.author, fullMessage)
                        del comboList
                if len(comboList) != 0 or comboList is not None:
                    fullMessage = "```" + tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid") + "```"
                    await client.send_message(message.author, fullMessage)
            else:
                await client.send_message(message.author, "The list is empty.")
        #LIST BIRTH DATES_END
        #BIRTHDAY ADDER_START
        if message.content.startswith(Prefix + "addBD"):
            command = str(message.content)[7:] # Removes the "!addBD " from the content
            userId = ""
            bd = ""
            if len(command.split()) == 2: # Needs the user id and date, so 2 parameters
                for parameter in command.split():
                    if "@" in parameter: # The UserId
                        userId = str(parameter)
                    elif "-" in parameter: # The BirthDate
                        bd = str(parameter)
                    else:
                        await client.send_message(message.channel, "**[@user](or <@!id>) or [mm-dd]** was not entered correctly.")
                        return
                try:
                    bdTest = datetime.strptime(bd, "%m-%d") # Verifying the date
                except ValueError:
                    await client.send_message(message.channel, "**Invalid date**, make sure you entered possible dates.")
                    return

                if not IsUserIdValid(m_MemberList, userId):
                    await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from this server.")
                    return

                await client.send_message(message.channel, "Added birthday.") # If this sends a message, it means everything is valid
            else:
                await client.send_message(message.channel, "Use the command this way : !addBD [@user](or <@!id>) [mm-dd]")
                return

            FileAddUserBD(m_UserBDList, userId, bd)
        #BIRTHDAY ADDER_END
        #BIRTHDAY REMOVER_START
        if message.content.startswith(Prefix + "removeBD"):
            #await client.send_message(message.channel, "Command deactivated.")
            #return #COMMMAND DEACTIVATED
            command = str(message.content)[10:] # Removes the "!removeBD " from the content
            userId = ""
            bd = ""
            if len(m_UserBDList) == 0:
                await client.send_message(message.channel, "There's nobody to remove from my birthday list.")
                return

            if len(command.split()) == 2: # Needs the user id and date, so 2 parameters
                for parameter in command.split():
                    if "@" in parameter: # The UserId
                        userId = str(parameter)
                    elif "-" in parameter: # The BirthDate
                        bd = str(parameter)
                    else:
                        await client.send_message(message.channel, "**[@user](or <@!id>) or [mm-dd]** was not entered correctly.")
                        return
                try:
                    bdTest = datetime.strptime(bd, "%m-%d") # Verifying the date
                except ValueError:
                    await client.send_message(message.channel, "**Invalid date**, make sure you entered possible dates.")
                    return

                if not IsUserIdValid(m_MemberList, userId):
                    await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from this server.")
                    return

            listIndex = 0 # We're sending the index to FileRemoveUserBD
            for userBd in m_UserBDList: # If the code reaches this, it means everything is valid
                if userId == userBd.userId and userBd.bd == bd:
                    FileRemoveUserBD(m_UserBDList, listIndex)
                    await client.send_message(message.channel, "Removed birthday.") 
                    return
                listIndex += 1
            await client.send_message(message.channel, "**User with this date is not in my list.**") 
        #BIRTHDAY REMOVER_END


client.loop.create_task(HappyBirthdayTimer())
client.run(Token())
