import asyncio
import platform
from re import *
from sys import exit
from subprocess import Popen
from datetime import datetime
from datetime import date
from util import *

try:
    import discord # https://github.com/Rapptz/discord.py
except ImportError:
    print("discord.py module not installed.\nhttps://github.com/Rapptz/discord.py")
    exit(1)

try:
    from tabulate import tabulate # https://pypi.python.org/pypi/tabulate
except ImportError:
    print("tabulate module not installed.\nhttps://pypi.python.org/pypi/tabulate")
    exit(1)

# TODO:
# - Move every command in another .py
# - Updates m_EmojiList, m_MemberList, m_ChannelList when one of them is added, removed or updated
# - Commands are case sensitive. Change it:
#           Now   -> "!WOh" != "!woh"
#           After -> "!WOh" == "!woh"
#
# - Custom prefix for every server
# - Enable or disable commands by doing something like this:
#           async def town(p_message : discord.Message, p_isActive : true)
#                               p_message -- message
#                               p_isActive -- if the commmand is active, true=on false=off
#
# - A way for my friends to use emoji reactions from my Emoji Server
#           Example: r:Loss: -> The bot will see this as a call for reaction,
#                               it will react with said emoji on the previous message.
#                               It will also remove the call.
#                               When they react afterwards, the bot will remove his reaction.
#                               In the future you will be able to choose which message with id or index.
#
# - Open and close my Terraria and Gmod server:
#           Send the Terraria console output on the channel made for it and recieve input
#
# - Optimization
# - Make everything easier to read

client = discord.Client()

def HappyBirthdayMessage(p_mm_dd : str, p_serverId : str):
    BdMessage = ""
    HappyB = "{} Happy Birthday ".format(ObtainEmojiWithName(m_EmojiList, "woh"))
    userBdToday = []

    # Checking the date and checking the user's server, then adding him/her to userBdToday[]: 
    for userBd in m_UserBDList:
        if p_mm_dd == userBd.bd and p_serverId == ObtainMemberInfo(m_MemberList, userBd.userId, "si", p_serverId):
            userBdToday.append(userBd)

    if len(userBdToday) != 0: # Checks if there's anyone in userBdToday[]
        for nbUser in userBdToday:
            BdMessage = BdMessage + HappyB + UserFormat(nbUser.userId) + "\n\n"
        return BdMessage
    else:
        return ""


async def HappyBirthdayTimer():
    await client.wait_until_ready()
    while not client.is_closed:
        mm_dd = str(date.today())[5:]
        for server in m_ServerList:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == server.id:
                    text = HappyBirthdayMessage(mm_dd, server.id)
                    if text != "":
                        await client.send_message(discord.Object(id=channelBD.channelId), text)

        today_n = datetime.today()
        today_t = datetime.today()
        try:
            today_t = today_n.replace(day=today_n.day + 1, hour=11, minute=0, second=0, microsecond=0)
        except ValueError:
            try:
                # Only time it will go there is at the end of the month, except December:
                today_t = today_n.replace(month=today_n.month + 1, day=1, hour=11, minute=0, second=0, microsecond=0)
            except ValueError:
                # Only time it will go there is on December 30th:
                today_t = today_n.replace(year=today_n.year + 1, month=1, day=1, hour=11, minute=0, second=0, microsecond=0)

        delta_secs = int((today_t - today_n).seconds + 1)
        print(today_n)
        await asyncio.sleep(delta_secs) # Task runs every day at 11h00am

    
@client.event
async def on_ready():
    ExtractInfo(client)
    print(ConsoleMessage(client))
    # Doesn't work, no idea why:
    # client.change_status(game=discord.Game(name="woh"))
    # client.change_presence(game="woh")
    game = discord.Game(name="{}woh for help".format(PREFIX))
    await client.change_presence(game=game, status=discord.Status.online)


@client.event
async def on_reaction_add(reaction, user):
    if False: 
        reaction = discord.Reaction() # Only there to help me, this breaks the bot
        user = discord.User()         # Only there to help me, this breaks the bot

    if user == client.user:
        return

    if reaction.emoji == ObtainEmojiWithName(m_EmojiList, "woh"):
        await client.add_reaction(reaction.message, reaction.emoji)


@client.event
async def on_message(message):
    if False:
        message = discord.Message(message) # Only there to help me, this breaks the bot

    if message.author == client.user: # This prevents the bot from responding to itself
        return

    #HELP WOH_START
    if message.content.startswith(PREFIX + "woh"):
        finalHelpMessage = HelpMessage # Normal
        if IsAdminUser(m_AdminUserList, message.author.id): # Admin
           finalHelpMessage += AdminHelpMessage
        if IsMe(message.author.id): # Owner
            finalHelpMessage += AdminHelpMessage + OwnerHelpMessage
        await client.send_message(message.author, finalHelpMessage)
    #HELP WOH_END

    #WOH REACTION_START
    if "woh" in message.content.lower():
        await client.add_reaction(message, ObtainEmojiWithName(m_EmojiList, "woh"))
    #WOH REACTION_END

    #OPEN CLOSE TEAMVIEWER_START
    if message.content.startswith(PREFIX + "openTV"):
        if IsMe(message.author.id):
            if platform.system() == 'Windows':
                proc = Popen(WindowsCmdOpenTV(), shell=True) # Opens TeamViewer.exe
                await client.send_message(message.channel, "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds.".format(SECONDS_TV))
                await asyncio.sleep(SECONDS_TV)
                proc.kill() # Closes TeamViewer.exe
                #await client.send_message(message.channel, "Closing TeamViewer...")
                return

            if platform.system() == 'Linux':
                proc = Popen(LinuxCmdOpenTV(), shell=True) # Opens TeamViewer.exe
                await client.send_message(message.channel, "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds.".format(SECONDS_TV))
                await asyncio.sleep(SECONDS_TV)
                proc.kill() # Closes TeamViewer.exe
                #await client.send_message(message.channel, "Closing TeamViewer...")
                return

            await client.send_message(message.channel, "**ERROR, host PC is not a Windows or Linux OS**")
    #OPEN CLOSE TEAMVIEWER_END

    #TOWN_START
    if message.content.startswith(PREFIX + "town") and message.server.id == MyServer():
        command = str(message.content)[6:] # Removes the "!town " from the content
        if len(command) != 0:
            msg = "Shut the Fuck Up Town\nPopulation: {}".format(command)
            await client.send_message(message.channel, msg)
            await client.delete_message(message)
    #TOWN_END
    #CITY_START
    if message.content.startswith(PREFIX + "city") and message.server.id == MyServer():
        command = str(message.content)[6:] # Removes the "!city " from the content
        if len(command) != 0:
            msg = "Gotem City\nPopulation: {}".format(command)
            await client.send_message(message.channel, msg)
            await client.delete_message(message)
    #CITY_END

    #BIRTHDAY CHANNEL DISPLAY_START
    if message.content.startswith(PREFIX + "showChannelBD"):
        if IsAdminUser(m_AdminUserList, message.author.id) or IsMe(message.author.id):
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == str(message.server.id):
                    await client.send_message(message.channel, "I send birthday messages to {}.".format(ChannelFormat(channelBD.channelId)))
                    return
            await client.send_message(message.channel, "I don't send birthday messages in this server.")
    #BIRTHDAY CHANNEL DISPLAY_END
    #BIRTHDAY CHANNEL ADDER_START    
    if message.content.startswith(PREFIX + "addChannelBD") and IsAdminUser(m_AdminUserList, message.author.id):
        if IsAdminUser(m_AdminUserList, message.author.id) or IsMe(message.author.id):
            channelId = str(message.content)[14:] # Removes the "!addChannelBD " from the content
            channelId = search("[0-9]{18}", channelId).group()
            if not IsChannelIdValid(m_ChannelList, channelId):
                await client.send_message(message.channel, "**Invalid channel**, make sure you entered a real channel from this server.")
                return
            
            for channelBD in m_ChannelBDList:
                if channelBD.channelId == channelId:
                    await client.send_message(message.channel, "**There's already a channel for birthday messages in this server**, delete the current one to change it.")
                    return

            # If this sends a message, it means everything is valid:
            await client.send_message(message.channel, "I will now send birthday messages in {}.".format(ChannelFormat(channelId)))
            FileAddChannelBD(m_ChannelBDList, channelId, str(message.server.id))
    #BIRTHDAY CHANNEL ADDER_END
    #BIRTHDAY CHANNEL REMOVER_START
    if message.content.startswith(PREFIX + "removeChannelBD") and IsAdminUser(m_AdminUserList, message.author.id):
        if IsAdminUser(m_AdminUserList, message.author.id) or IsMe(message.author.id):
            serverId = str(message.server.id)   
            listIndex = 0 # We're sending the index to FileRemoveChannelBD
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == serverId:
                    FileRemoveChannelBD(m_ChannelBDList, listIndex)
                    await client.send_message(message.channel, "I will no longer send birthday messages in this server.")
                    return
                listIndex += 1
            await client.send_message(message.channel, "There's no channel to remove.")
    #BIRTHDAY CHANNEL REMOVER_END

    #LIST ADMIN USERS_START
    if message.content.startswith(PREFIX + "listAdminUser"):
        if IsMe(message.author.id):
            serverId = str(message.server.id)
            if len(m_AdminUserList) != 0:
                comboList = []
                for adminUser in m_AdminUserList:
                    if serverId == ObtainMemberInfo(m_MemberList, adminUser, "si", serverId):
                        name = ObtainMemberInfo(m_MemberList, adminUser, "na", "")
                        comboList.append([name])
                    if len(comboList) == 10:
                        fullMessage = CodeFormat(tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                        await client.send_message(message.author, fullMessage)
                        del comboList
                if len(comboList) != 0 or comboList is not None:
                    fullMessage = CodeFormat(tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                    await client.send_message(message.author, fullMessage)
            else: 
                await client.send_message(message.author, "The list is empty.")
    #LIST ADMIN USERS_END
    #ADMIN USER ADDER_START
    if message.content.startswith(PREFIX + "addAdminUser"):
        if IsMe(message.author.id):
            userId = str(message.content)[14:] # Removes the "!addAdminUser " from the content
            userId = search("[0-9]{18}", userId).group()
            if not IsUserIdValid(m_MemberList, userId):
                await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from this server.")
                return

            for adminUser in m_AdminUserList:
                if ObtainMemberInfo(m_MemberList, userId, "id", "") == adminUser:
                    await client.send_message(message.channel, "You're already an admin.")
                    return
                
            await client.send_message(message.channel, "Admin Added.".format(UserFormat(userId)))
            FileAddAdminUser(m_AdminUserList, userId)
    #ADMIN USER ADDED_END
    #ADMIN USER REMOVER_START
    if message.content.startswith(PREFIX + "removeAdminUser"):
        if IsMe(message.author.id):
            userId = str(message.content)[17:] # Removes the "!removeAdminUser " from the content
            userId = re.search("[0-9]{18}", userId).group()
            if not IsUserIdValid(m_MemberList, userId):
                await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from this server.")
                return

            listIndex = 0
            for adminUser in m_AdminUserList:
                if ObtainMemberInfo(m_MemberList, userId, "id", "") == adminUser:
                    FileRemoveAdminUser(m_AdminUserList, listIndex)
                    await client.send_message(message.channel, "Removed Admin commands.")
                    return
                listIndex += 1
            await client.send_message(message.channel, "Can't remove the user if he's not in the list.")
    #ADMIN USER REMOVER_END

    #LIST BIRTH DATES_START
    if message.content.startswith(PREFIX + "listUserBD"):
        serverId = str(message.server.id)
        if len(m_UserBDList) != 0:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == serverId:
                    comboList = []
                    for userBd in m_UserBDList:
                        if serverId == ObtainMemberInfo(m_MemberList, userBd.userId, "si", serverId):
                            name = ObtainMemberInfo(m_MemberList, userBd.userId, "na", "")
                            comboList.append([name, userBd.bd])
                        if len(comboList) == 10:
                            fullMessage = CodeFormat(tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"), "")
                            await client.send_message(message.author, fullMessage)
                            del comboList
                    if len(comboList) != 0 or comboList is not None:
                        fullMessage = CodeFormat(tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"), "")
                        await client.send_message(message.author, fullMessage)
        else: 
            await client.send_message(message.author, "The list is empty.")
    #LIST BIRTH DATES_END
    #BIRTHDAY ADDER_START    
    if message.content.startswith(PREFIX + "addUserBD"):
        for userBd in m_UserBDList:
            if ObtainMemberInfo(m_MemberList, str(message.author.id), "id", "") == userBd.userId:
                await client.send_message(message.channel, "You're already in my list")
                return
        command = str(message.content)[14:] # Removes the "!addUserBD " from the content
        userId = str(message.author.id)
        bd = str(command)

        try:
            bdTest = datetime.strptime(bd, "%m-%d") # Verifying the date
        except ValueError:
            await client.send_message(message.channel, "**Invalid date**, make sure you entered possible dates.")
            return

        if not IsUserIdValid(m_MemberList, userId):
            await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from this server.")
            return

        FileAddUserBD(m_UserBDList, userId, bd)
        await client.send_message(message.channel, "Added birthday.") # If this sends a message, it means everything is valid
    #BIRTHDAY ADDER_END
    #BIRTHDAY REMOVER_START
    if message.content.startswith(PREFIX + "removeChannelBD"):
        userId = str(message.author.id)
        listIndex = 0 # We're sending the index to FileRemoveUserBD
        for userBd in m_UserBDList:
            if userBd.userId == userId:
                FileRemoveUserBD(m_UserBDList, listIndex)
                await client.send_message(message.channel, "You are no longer in my birthday list.")
                return
            listIndex += 1
        await client.send_message(message.channel, "Can't remove you if you're not in my list.")
    #BIRTHDAY REMOVER_END


client.loop.create_task(HappyBirthdayTimer())
client.run(Token())
