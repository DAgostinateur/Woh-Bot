"""Tools for Woh_Bot_Main.py"""
try:
    import discord # https://github.com/Rapptz/discord.py
except ImportError:
    print("discord.py module not installed.\nhttps://github.com/Rapptz/discord.py")
    exit(1)

import os
import json
import asyncio
import platform
from inspect import stack
from re import *
from sys import exit
from subprocess import Popen
from datetime import datetime
from datetime import date
from hidden import * # Things I don't want seen by the public.

try:
    from tabulate import tabulate # https://pypi.python.org/pypi/tabulate
except ImportError:
    print("tabulate module not installed.\nhttps://pypi.python.org/pypi/tabulate")
    exit(1)

def myself():
    """Returns the name of the parent method.""" 
    return str(stack()[1][3])

PREFIX = '!'     # The prefix that will be used for commands
ID_LENGTH = 18   # Length of a Discord Id
SECONDS_TV = 600 # Number of seconds before closing TeamViewer

def ConsoleMessage(p_client):
    return """-----------
Woh Bot
-----------
Logged in as {}
Creator : D'Agostinateur Woh
-----------""".format(str(p_client.user))

m_ServerList = []    # List of every Server Woh Bot is in
m_ChannelList = []   # List of every Channel Woh Bot has access to
m_EmojiList = []     #               Emoji
m_MemberList = []    #               Member 
m_UserBDList = []    #               UserBD
m_ChannelBDList = [] #               ChannelBD
m_AdminUserList = [] #               Admin User

class UserBD(list):
    """A UserBD is made of a user and their birthday date."""
    def __init__(self, userId, bd):
        """Keyword arguments:
        userId -- user ID, Format: 000000000000000000
        bd     -- birthday date, Format: mm-dd"""
        self.bd = bd
        self.userId = userId


class ChannelBD(list):
    """A ChannelBD is made of a channel id and a server id."""
    def __init__(self, channelId, serverId):
        """Keyword arguments:
        channelId -- channel ID, Format: 000000000000000000
        serverId  -- server ID,  Format: 000000000000000000"""
        self.serverId = serverId
        self.channelId = channelId


class AdminUser(list): # Will be used in the future
    """An AdminUser is made of a user id and a server id."""
    def __init__(self, userId, serverId):
        """Keyword arguments:
        userId    -- user ID,   Format: 000000000000000000
        serverId  -- server ID, Format: 000000000000000000"""
        self.userId = userId
        self.serverId = serverId


def CodeFormat(p_string, p_code : ""):
    """Returns the string in code format.
    Format: ```code
            string```

    Keyword arguments:
    p_content -- content of the message
    p_code    -- code for the format"""
    return "```{}\n".format(p_code) + p_string + "```"
    
def UserFormat(p_userId):
    """Returns the id in user format.
    Format: <@id>

    Keyword arguments:
    p_userId -- user id"""
    return "<@" + p_userId + ">"

def ChannelFormat(p_channelId):
    """Returns the id in channel format.
    Format: <#id>

    Keyword arguments:
    p_channelId -- channel id"""
    return "<#" + p_channelId + ">"

def ObtainServerCount(p_ServerList, p_serverId : str):
    """Returns the number of humans in a server.
    
    Keyword arguments:
    p_ServerList -- server list
    p_serverId   -- server Id"""
    humanCount = 0
    for server in m_ServerList:
        if server.id == p_serverId:
            for member in server.members:
                if not member.bot:
                    humanCount += 1
            break
    return humanCount

def ObtainEmojiWithName(p_EmojiList, p_name : str):
    """Returns the emoji from the emoji list with the name of it.
    Returns 'octagonal_sign' if the name is wrongly entered.
    
    Keyword arguments:
    p_EmojiList -- emoji list
    p_name      -- name of emoji"""
    for emoji in p_EmojiList:
        if emoji.name == p_name: 
            return emoji
    return "octagonal_sign" # If the bot ever uses this, that means I typed the name wrong


def ObtainChannelInfo(p_ChannelList, p_id : str, p_mode : "ch"):
    """Obtains Information from a channel.
    
    Keyword arguments:
    p_ChannelList -- channel list
    p_id          -- channel.id
    p_mode        -- different mode returns different objects

    Modes:
    ch - Returns a Channel (DEFAULT)
    id - Returns a Channel.id
    na - Returns a Channel.name
    Returns -1 and notifies you in console if the mode is wrongly entered."""
    # Checks the list for the channel with the "p_id"
    if p_mode == "ch":
        for channel in p_ChannelList:
            if channel.id == p_id: 
                return channel      # Returns a Channel object
    elif p_mode == "id": # This is a verification
        for channel in p_ChannelList:
            if channel.id == p_id: 
                return channel.id   # Returns the id
    elif p_mode == "na":
        for channel in p_ChannelList:
            if channel.id == p_id: 
                return channel.name # Returns the name
    else:
        print("{} MODE DOESN'T EXIST (ObtainChannelInfo)".format(p_mode))
        return "-1"


def ObtainMemberInfo(p_MemberList, p_id : str, p_mode : "mb", p_serverId : ""):
    """Obtains Information from a member.
    
    Keyword arguments:
    p_MemberList -- member list
    p_id         -- member.id
    p_mode       -- different mode returns different objects
    p_serverId   -- server id (for 'si' mode)

    Modes:
    mb - Returns a Member (DEFAULT)
    id - Returns a Member.id
    na - Returns a Member.name
    nl - Returns the length of Member.name
    si - Returns a Member.server.id
    Returns -1 and notifies you in console if the mode is wrongly entered."""
    # Checks the list for the member with the "p_id"
    if p_mode == "mb":
        for member in p_MemberList:
            if member.id == p_id: 
                return member           # Returns a Member object
    elif p_mode == "id": # This is a verification
        for member in p_MemberList:
            if member.id == p_id: 
                return member.id        # Returns the id
    elif p_mode == "na":
        for member in p_MemberList:
            if member.id == p_id: 
                return member.name      # Returns the name
    elif p_mode == "nl":
        for member in p_MemberList:
            if member.id == p_id: 
                return len(member.name) # Returns the length of the name
    elif p_mode == "si": # This is a verification
        for member in p_MemberList:
            if member.id == p_id and member.server.id == p_serverId: 
                return member.server.id # Returns the server id of the member.
    else:
        print("{} MODE DOESN'T EXIST (ObtainMemberInfo)".format(p_mode))
        return "-1"


def IsUserIdValid(p_MemberList, p_userId : str):
    """True = Valid
    False = Not valid
    UserId is valid if : It has 18 digits and an existing channel.
    Accepts only digits.

    Keyword arguments:
    p_MemberList -- member list
    p_id         -- member.id"""
    if len(p_userId) == ID_LENGTH and p_userId == ObtainMemberInfo(p_MemberList, p_userId, "id", ""):
        return True
    return False


def IsChannelIdValid(p_ChannelList, p_channelId : str):
    """True = Valid
    False = Not valid
    ChannelId is valid if : It has 18 digits and an existing member.
    Accepts only digits.
    
    Keyword arguments:
    p_ChannelList -- channel list
    p_channelId   -- channel.id"""
    if len(p_channelId) == ID_LENGTH and p_channelId == ObtainChannelInfo(p_ChannelList, numberId, "id"):
        return True
    return False


def IsAdminUser(p_adminUserList, p_userId : str):
    """Verifies if the userId is an admin.
    
    Keyword arguments:
    p_adminUserList -- admin user list
    p_userId        -- user id"""
    for adminUser in p_adminUserList:
        if adminUser == p_userId:
            return True
    return False

def IsMe(p_userId : str):
    """Verifies if the userId is an admin.
    
    Keyword arguments:
    p_userId -- user id"""
    if p_userId == MyID():
        return True
    return False

#####################
#     FILE_START    #
#####################

#FileUserBD_START
def FileExtractUserBD(p_userBDList):
    """Extracts the content of FileNameUserBD() 
    and puts it in the list.
    
    Keyword arguments:
    p_userBDList -- userBd list"""
    del p_userBDList[:]
    with open(FileNameUserBD(), 'r') as file:
        if os.stat(FileNameUserBD()).st_size == 0: # If the file is empty
            return

        listDicts = json.load(file)
        for d in listDicts:
            p_userBDList.append(UserBD(d['userId'], d['bd']))

def FileRemoveUserBD(p_userBDList, p_listIndex : int):
    """Removes the content of the list at index
    and writes the list in FileNameUserBD().
    
    Keyword arguments:
    p_userBDList -- userBd list
    p_listIndex  -- remove object at index"""
    del p_userBDList[p_listIndex]
    listDicts = [{'userId': x.userId, 'bd': x.bd} for x in p_userBDList]
    json_string = json.dumps(listDicts, indent=4, separators=(',', ' : '))
    with open(FileNameUserBD(), 'w') as file:
        file.write(json_string)

    print("List of UserBD has been updated. A UserBD has been removed.")

def FileAddUserBD(p_userBDList, p_userId : str, p_bd : str):
    """Adds the user id and bd to the list
    and writes it in FileNameUserBD().
    
    Keyword arguments:
    p_userBDList -- userBd list
    userId -- user id
    bd     -- birthday date"""
    p_userBDList.append(UserBD(p_userId, p_bd))
    listDicts = [{'userId': x.userId, 'bd': x.bd} for x in p_userBDList]
    json_string = json.dumps(listDicts, indent=4, separators=(',', ' : '))
    with open(FileNameUserBD(), 'w') as file:
        file.write(json_string)

    print("List of UserBD has been updated. A UserBD has been added.")
#FileUserBD_END

#FileChannelBD_START
def FileExtractChannelBD(p_channelBDList):
    """Extracts the content of FileNameChannelBD() 
    and puts it in the list.
    
    Keyword arguments:
    p_channelBDList -- channelBd list"""
    del p_channelBDList[:]
    with open(FileNameChannelBD(), 'r') as file:
        if os.stat(FileNameChannelBD()).st_size == 0:
            return

        listDicts = json.load(file)
        for d in listDicts:
            p_channelBDList.append(ChannelBD(d['channelId'], d['serverId']))

def FileRemoveChannelBD(p_channelBDList, p_listIndex : int):
    """Removes the content of the list at index
    and writes the list in FileNameChannelBD().
    
    Keyword arguments:
    p_channelBDList -- channelBd list
    p_listIndex     -- remove object at index"""
    del p_channelBDList[p_listIndex]
    listDicts = [{'channelId': x.channelId, 'serverId': x.serverId} for x in p_channelBDList]
    json_string = json.dumps(listDicts, indent=4, separators=(',', ' : '))
    with open(FileNameChannelBD(), 'w') as file:
        file.write(json_string)

    print("List of ChannelBD has been updated. A ChannelBD has been removed.")

def FileAddChannelBD(p_channelBDList, p_channelId : str, p_serverId : str):
    """Adds the channel id and server id to the list
    and writes it in FileNameChannelBD().
    
    Keyword arguments:
    p_channelBDList -- channelBd list
    p_channelId     -- channel id
    p_serverId      -- server id"""
    p_channelBDList.append(ChannelBD(p_channelId, p_serverId))
    listDicts = [{'channelId': x.channelId, 'serverId': x.serverId} for x in p_channelBDList]
    json_string = json.dumps(listDicts, indent=4, separators=(',', ' : '))
    with open(FileNameChannelBD(), 'w') as file:
        file.write(json_string)

    print("List of ChannelBD has been updated. A ChannelBD has been added.")
#FileChannelBD_END

#FileAdminUser_START
def FileExtractAdminUser(p_adminUserList):
    """Extracts the content of FileNameAdminUser() 
    and puts it in the list.
    
    Keyword arguments:
    p_adminUserList -- adminUser list"""
    del p_adminUserList[:]
    with open(FileNameAdminUser(), 'r') as file:
        if os.stat(FileNameAdminUser()).st_size == 0:
            return

        listDicts = json.load(file)
        for d in listDicts:
            p_adminUserList.append(d['userId'])

def FileRemoveAdminUser(p_adminUserList, p_listIndex : int):
    """Removes the content of the list at index
    and writes the list in FileNameAdminUser().
    
    Keyword arguments:
    p_adminUserList -- adminUser list
    p_listIndex     -- remove object at index"""
    del p_adminUserList[p_listIndex]
    listDicts = [{'userId': x} for x in p_adminUserList]
    json_string = json.dumps(listDicts, indent=4, separators=(',', ' : '))
    with open(FileNameAdminUser(), 'w') as file:
        file.write(json_string)

    print("List of AdminUser has been updated. A AdminUser has been removed.")

def FileAddAdminUser(p_adminUserList, p_adminUser : str):
    """Adds the adminUser id to the list
    and writes it in FileNameAdminUser().
    
    Keyword arguments:
    p_adminUserList -- adminUser list
    adminUser       -- adminUser id"""
    p_adminUserList.append(p_adminUser)
    listDicts = [{'userId': x} for x in p_adminUserList]
    json_string = json.dumps(listDicts, indent=4, separators=(',', ' : '))
    with open(FileNameAdminUser(), 'w') as file:
        file.write(json_string)

    print("List of AdminUser has been updated. A AdminUser has been added.")
#FileAdminUser_END

#####################
#      FILE_END     #
#####################

def ExtractInfo(p_client):
    """Fills up every member list.
    
    Keyword arguments:
    p_client -- discord client"""
    for server in p_client.servers:
        m_ServerList.append(server)       # Colects every Server
        for channel in server.channels:
            m_ChannelList.append(channel) # Collects every Channel from every server
        for emoji in server.emojis: 
            m_EmojiList.append(emoji)     # Collects every Emoji from every server
        for member in server.members: 
            m_MemberList.append(member)   # Collects every Member from every server

    FileExtractUserBD(m_UserBDList)       # Collects every UserBd from FileNameUserBD()
    FileExtractChannelBD(m_ChannelBDList) # Collects every ChannelBd from FileNameChannelBD()
    FileExtractAdminUser(m_AdminUserList) # Collects every AdminUser from FileNameAdminUser()
    print("""List of Servers has been extracted.
List of Channels has been extracted.
List of Emojis has been extracted.
List of Members has been extracted.
List of UserBD has been extracted.
List of ChannelBD has been extracted.
List of AdminUser has been extracted.""")
