import os
import json
import constants
from hidden import *
from util import UserBD, AdminUser, ChannelBD

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

    print(constants.USER_BD_REMOVED_STRING)

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

    print(constants.USER_BD_ADDED_STRING)
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

    print(constants.CHANNEL_BD_REMOVED_STRING)

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

    print(constants.CHANNEL_BD_ADDED_STRING)
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

    print(constants.ADMIN_USER_REMOVED_STRING)

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

    print(constants.ADMIN_USER_ADDED_STRING)
#FileAdminUser_END