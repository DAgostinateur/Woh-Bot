"""Tools for Woh_Bot_Main.py"""
import discord
from hidden import *

class UserBD(list):
    """A UserBD is made of an id from a user and his/her birthday date."""
    def __init__(self, userId, bd):
        """Keyword arguments:
        userId -- user ID, Format: <@!000000000000000000>
        bd -- birthday date, Format: mm-dd"""
        self.bd = bd
        self.userId = userId

    def ObtainPureUserID(self):
        """Obtains the pure id from UserBD.userId.
        Example: <@!000000000000000000> -> 000000000000000000"""
        return str(self.userId[3:21])

class ChannelBD(list):
    """A ChannelBD is made of a channel id and a server id."""
    def __int__(self, channelId, serverId):
        """Keyword arguments:
        channelId -- channel ID, Format: <#000000000000000000>
        serverId -- server ID, Format: 000000000000000000"""
        self.serverId = serverId
        self.channelId = channelId

    def ObtainPureChannelID(self):
        """Obtains the pure id from ChannelBD.channelId.
        Example: <#000000000000000000> -> 000000000000000000"""
        return str(self.channelId[2:20])


def ObtainEmojiWithName(p_EmojiList, p_name : str):
    """Returns the emoji from the emoji list with the name of it.
    Returns 'octagonal_sign' if the name is wrongly entered.
    
    Keyword arguments:
    p_EmojiList -- emoji list
    p_name -- name of emoji"""
    for emoji in p_EmojiList:
        if emoji.name == p_name:
            return emoji
    return "octagonal_sign" #If the bot ever uses this, that means I typed the name wrong

def ObtainHighestMemberName(p_MemberList):
    """Returns the length of the longest Member.name in the MemberList.
    
    Keyword arguments:
    p_MemberList -- member list"""
    length = 0
    for member in p_MemberList:
        nameLength = len(member.name)
        if nameLength > length:
            length = nameLength
    return length

def ObtainMemberInfo(p_MemberList, p_id : str, p_mode : "mb"):
    """Obtains Information from a member.
    
    Keyword arguments:
    p_MemberList -- member list
    p_id -- member.id
    p_mode -- different mode returns different objects

    Modes:
    mb - Returns a Member (DEFAULT)
    id - Returns a Member.id
    na - Returns a Member.name
    nl - Returns the length of Member.name
    Returns -1 and notifies you in console if the mode is wrongly entered."""
    #Checks the list for the member with the "p_id"
    if p_mode == "mb":
        for member in p_MemberList:
            if member.id == p_id:
                return member #Returns a Member object
    elif p_mode == "id": #This is a verification
        for member in p_MemberList:
            if member.id == p_id:
                return member.id #Returns the id
    elif p_mode == "na":
        for member in p_MemberList:
            if member.id == p_id:
                return member.name #Returns the name
    elif p_mode == "nl":
        for member in p_MemberList:
            if member.id == p_id:
                return len(member.name) #Returns the length of the name
    else:
        print("{} MODE DOESN'T EXIST (ObtainMemberInfo)".format(p_mode))
        return "-1"

def IsUserIdValid(p_MemberList, p_userId : str):
    """True = Valid
    False = Not valid
    UserId is valid if : It starts with '<@!', ends with '>' and has 18
    numbers in between.
    
    Keyword arguments:
    p_MemberList -- member list
    p_id -- member.id"""
    p_userId = str(p_userId)
    numberId = p_userId[3:21]
    if p_userId.startswith("<@!") and p_userId.endswith(">") and numberId.isdigit():
        if numberId == ObtainMemberInfo(p_MemberList, numberId, "id"):
            return True
    return False

#####################
# FILE MANIPULATION #
#####################
def FileExtractBD(p_userBDList):
    """Extracts the content of data.txt 
    and puts it in the list.
    
    Keyword arguments:
    p_userBDList -- userBd list"""
    with open(FileNameUserBD(), 'r') as file:
        del p_userBDList[:]
        content = file.readlines() #Copies every line in this variable, which is a list
        content = [x.strip("\n") for x in content] #Removes \n from these lines
        for line in content:
            lineBD = line.split('|') #Seperates userId and bd
            p_userBDList.append(UserBD(lineBD[0], lineBD[1]))

def FileRemoveBD(p_userBDList, p_listIndex : int):
    """Removes the content of the list at index
    and writes the list in data.txt.
    
    Keyword arguments:
    p_userBDList -- userBd list
    p_listIndex -- remove object at index"""
    del p_userBDList[p_listIndex]
    with open(FileNameUserBD(), 'w') as file:
        index = 0
        for userBd in p_userBDList:
            if index == 0:
                file.write("{}|{}".format(userBd.userId, userBd.bd))
            else:
                file.write("\n{}|{}".format(userBd.userId, userBd.bd))
            index += 1
    print("List of UserBD has been updated. A UserBD has been removed.")

def FileAddBD(p_userBDList, p_userId : str, p_bd : str):
    """Adds the user id and bd to the list
    and writes it in data.txt.
    
    Keyword arguments:
    p_userBDList -- userBd list
    userId -- user id
    bd -- birthday date"""
    p_userBDList.append(UserBD(p_userId, p_bd))
    with open(FileNameUserBD(), 'a') as file:
        file.write("\n{}|{}".format(p_userId, p_bd))
    print("List of UserBD has been updated. A UserBD has been added.")
