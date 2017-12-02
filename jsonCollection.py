import os
import json
import constants
import hidden
from specialClasses import *


def file_extract_user_bd(p_user_bd_list):
    """Extracts the content of FileNameUserBD() 
    and puts it in the list.
    
    Keyword arguments:
    p_user_bd_list -- userBd list"""
    del p_user_bd_list[:]
    with open(hidden.file_name_user_bd(), 'r') as file:
        if os.stat(hidden.file_name_user_bd()).st_size == 0:  # If the file is empty
            return

        list_dicts = json.load(file)
        for d in list_dicts:
            p_user_bd_list.append(UserBD(d['userId'], d['bd']))


def file_remove_user_bd(p_user_b_list, p_list_index: int):
    """Removes the content of the list at index
    and writes the list in FileNameUserBD().
    
    Keyword arguments:
    p_user_b_list -- userBd list
    p_list_index  -- remove object at index"""
    del p_user_b_list[p_list_index]
    list_dicts = [{'userId': x.userId, 'bd': x.bd} for x in p_user_b_list]
    json_string = json.dumps(list_dicts, indent=4, separators=(',', ' : '))
    with open(hidden.file_name_user_bd(), 'w') as file:
        file.write(json_string)

    print(constants.USER_BD_REMOVED_STRING)


def file_add_user_bd(p_user_bd_list, p_user_id: str, p_bd: str):
    """Adds the user id and bd to the list
    and writes it in FileNameUserBD().
    
    Keyword arguments:
    p_user_bd_list -- userBd list
    userId -- user id
    bd     -- birthday date"""
    p_user_bd_list.append(UserBD(p_user_id, p_bd))
    list_dicts = [{'userId': x.userId, 'bd': x.bd} for x in p_user_bd_list]
    json_string = json.dumps(list_dicts, indent=4, separators=(',', ' : '))
    with open(hidden.file_name_user_bd(), 'w') as file:
        file.write(json_string)

    print(constants.USER_BD_ADDED_STRING)


def file_extract_channel_bd(p_channel_bd_list):
    """Extracts the content of FileNameChannelBD() 
    and puts it in the list.
    
    Keyword arguments:
    p_channel_bd_list -- channelBd list"""
    del p_channel_bd_list[:]
    with open(hidden.file_name_channel_bd(), 'r') as file:
        if os.stat(hidden.file_name_channel_bd()).st_size == 0:
            return

        list_dicts = json.load(file)
        for d in list_dicts:
            p_channel_bd_list.append(ChannelBD(d['channelId'], d['serverId']))


def file_remove_channel_bd(p_channel_bd_list, p_list_index: int):
    """Removes the content of the list at index
    and writes the list in FileNameChannelBD().
    
    Keyword arguments:
    p_channel_bd_list -- channelBd list
    p_list_index     -- remove object at index"""
    del p_channel_bd_list[p_list_index]
    list_dicts = [{'channelId': x.channelId, 'serverId': x.serverId} for x in p_channel_bd_list]
    json_string = json.dumps(list_dicts, indent=4, separators=(',', ' : '))
    with open(hidden.file_name_channel_bd(), 'w') as file:
        file.write(json_string)

    print(constants.CHANNEL_BD_REMOVED_STRING)


def file_add_channel_bd(p_channel_bd_list, p_channel_id: str, p_server_id: str):
    """Adds the channel id and server id to the list
    and writes it in FileNameChannelBD().
    
    Keyword arguments:
    p_channel_bd_list -- channelBd list
    p_channel_id     -- channel id
    p_server_id      -- server id"""
    p_channel_bd_list.append(ChannelBD(p_channel_id, p_server_id))
    list_dicts = [{'channelId': x.channelId, 'serverId': x.serverId} for x in p_channel_bd_list]
    json_string = json.dumps(list_dicts, indent=4, separators=(',', ' : '))
    with open(hidden.file_name_channel_bd(), 'w') as file:
        file.write(json_string)

    print(constants.CHANNEL_BD_ADDED_STRING)


def file_extract_admin_user(p_admin_user_list):
    """Extracts the content of FileNameAdminUser() 
    and puts it in the list.
    
    Keyword arguments:
    p_admin_user_list -- adminUser list"""
    del p_admin_user_list[:]
    with open(hidden.file_name_admin_user(), 'r') as file:
        if os.stat(hidden.file_name_admin_user()).st_size == 0:
            return

        list_dicts = json.load(file)
        for d in list_dicts:
            p_admin_user_list.append(d['userId'])


def file_remove_admin_user(p_admin_user_list, p_list_index: int):
    """Removes the content of the list at index
    and writes the list in FileNameAdminUser().
    
    Keyword arguments:
    p_admin_user_list -- adminUser list
    p_list_index     -- remove object at index"""
    del p_admin_user_list[p_list_index]
    list_dicts = [{'userId': x} for x in p_admin_user_list]
    json_string = json.dumps(list_dicts, indent=4, separators=(',', ' : '))
    with open(hidden.file_name_admin_user(), 'w') as file:
        file.write(json_string)

    print(constants.ADMIN_USER_REMOVED_STRING)


def file_add_admin_user(p_admin_user_list, p_admin_user: str):
    """Adds the adminUser id to the list
    and writes it in FileNameAdminUser().
    
    Keyword arguments:
    p_admin_user_list -- adminUser list
    adminUser       -- adminUser id"""
    p_admin_user_list.append(p_admin_user)
    list_dicts = [{'userId': x} for x in p_admin_user_list]
    json_string = json.dumps(list_dicts, indent=4, separators=(',', ' : '))
    with open(hidden.file_name_admin_user(), 'w') as file:
        file.write(json_string)

    print(constants.ADMIN_USER_ADDED_STRING)
