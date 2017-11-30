"""Tools for WohBot.py"""
from sys import exit

try:
    import discord # https://github.com/Rapptz/discord.py
except ImportError:
    print("discord.py module not installed.\nhttps://github.com/Rapptz/discord.py")
    exit(1)

try:
    import tabulate # https://pypi.python.org/pypi/tabulate
except ImportError:
    print("tabulate module not installed.\nhttps://pypi.python.org/pypi/tabulate")
    exit(1)

import asyncio
import platform
from inspect import stack
from re import *
from subprocess import Popen
from datetime import datetime
from datetime import date
from hidden import * # Things I don't want seen by the public.
from constants import *


def myself():
    """Returns the name of the parent method.""" 
    return str(stack()[1][3])

tabulate.PRESERVE_WHITESPACE = True

m_ServerList = []    # List of Server Woh Bot is in
m_UserBDList = []    # List of UserBD
m_ChannelBDList = [] # List of ChannelBD
m_AdminUserList = [] # List of Admin User

m_NormalMessage = []   # Using strings doesn't work :(
m_AdminMessage = []    # So I have to use a silly hack
m_OwnerMessage = []    # Using lists of 1 item instead

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

import jsonCollection

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

def ObtainServerCount(p_server):
    """Returns the number of humans in a server.
    
    Keyword arguments:
    p_ServerList -- server list"""
    humanCount = 0
    for member in p_server.members:
        if not member.bot:
            humanCount += 1
    return humanCount

def ObtainEmojiWithName(p_EmojiList, p_name : str):
    """Returns the emoji from the emoji list with the name of it.
    Returns 'octagonal_sign' if the name is wrongly entered.
    
    Keyword arguments:
    p_EmojiList -- emoji list
    p_name      -- name of emoji"""
    for emoji in p_EmojiList:
        if emoji.name.lower() == p_name.lower(): 
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

def ExtractInfo(p_client, p_wCommand):
    """Fills up every member list.
    
    Keyword arguments:
    p_client   -- main discord.Client()
    p_wCommand --  main WComand()"""
    m_NormalMessage.append(p_wCommand.normalMessage())
    m_AdminMessage.append(p_wCommand.adminMessage())
    m_OwnerMessage.append(p_wCommand.ownerMessage())

    for server in p_client.servers:
        m_ServerList.append(server) # Gets every Server

    jsonCollection.FileExtractUserBD(m_UserBDList)       # Gets every UserBd from FileNameUserBD()
    jsonCollection.FileExtractChannelBD(m_ChannelBDList) # Gets every ChannelBd from FileNameChannelBD()
    jsonCollection.FileExtractAdminUser(m_AdminUserList) # Gets every AdminUser from FileNameAdminUser()
    print(JSON_COLLECTION_MESSAGE)
