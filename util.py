"""Tools for WohBot.py"""
from sys import exit


try:
    import discord  # https://github.com/Rapptz/discord.py
except ImportError:
    print("discord.py module not installed.\nhttps://github.com/Rapptz/discord.py")
    exit(1)

try:
    # noinspection PyUnresolvedReferences
    import tabulate  # https://pypi.python.org/pypi/tabulate
except ImportError:
    print("tabulate module not installed.\nhttps://pypi.python.org/pypi/tabulate")
    exit(1)

from inspect import stack
from datetime import datetime
from hidden import *  # Things I don't want seen by the public.
from constants import *
import jsonCollection


def myself():
    """Returns the name of the parent method."""
    return str(stack()[1][3])


tabulate.PRESERVE_WHITESPACE = True

m_ServerList = []  # List of Server Woh Bot is in
m_UserBDList = []  # List of UserBD
m_ChannelBDList = []  # List of ChannelBD
m_AdminUserList = []  # List of Admin User

m_NormalMessage = []  # Using strings doesn't work :(
m_AdminMessage = []  # So I have to use a silly hack
m_OwnerMessage = []  # Using lists of 1 item instead


def code_format(p_content, p_code=""):
    """Returns the string in code format.
    Format: ```p_code
            p_content```

    Keyword arguments:
    p_content -- content of the message
    p_code    -- code for the format"""
    return "```{0}\n".format(p_code) + p_content + "```"


def user_format(p_user_id):
    """Returns the id in user format.
    Format: <@id>

    Keyword arguments:
    p_user_id -- user id"""
    return "<@" + p_user_id + ">"


def channel_format(p_channel_id):
    """Returns the id in channel format.
    Format: <#id>

    Keyword arguments:
    p_channel_id -- channel id"""
    return "<#" + p_channel_id + ">"


def obtain_server_count(p_server):
    """Returns the number of humans in a server.
    
    Keyword arguments:
    p_ServerList -- server list"""
    human_count = 0
    for member in p_server.members:
        if not member.bot:
            human_count += 1
    return human_count


def get_next_day_delta(p_hour: int):
    """Calculate the delta.
    
    Keyword arguments:
    p_hour -- hour in the day"""
    today_n = datetime.today()
    try:
        today_t = today_n.replace(day=today_n.day + 1, hour=p_hour, minute=0, second=0, microsecond=0)
    except ValueError:
        try:
            # Only time it will go there is at the end of the month, except December:
            today_t = today_n.replace(month=today_n.month + 1, day=1, hour=p_hour, minute=0, second=0, microsecond=0)
        except ValueError:
            # Only time it will go there is on December 30th:
            today_t = today_n.replace(year=today_n.year + 1, month=1, day=1, hour=p_hour, minute=0, second=0,
                                      microsecond=0)
    return int((today_t - today_n).seconds + 1)


def obtain_emoji_with_name(p_emoji_list, p_name: str):
    """Returns the emoji from the emoji list with the name of it.
    Returns 'octagonal_sign' if the name is wrongly entered.
    
    Keyword arguments:
    p_emoji_list -- emoji list
    p_name      -- name of emoji"""
    for emoji in p_emoji_list:
        if emoji.name.lower() == p_name.lower():
            return emoji
    return "octagonal_sign"  # If the bot ever uses this, that means I typed the name wrong


def obtain_channel_info(p_channel_list, p_id: str, p_mode="ch"):
    """Obtains Information from a channel.
    
    Keyword arguments:
    p_channel_list -- channel list
    p_id          -- channel.id
    p_mode        -- different mode returns different objects

    Modes:
    ch - Returns a Channel (DEFAULT)
    id - Returns a Channel.id
    na - Returns a Channel.name
    Returns -1 and notifies you in console if the mode is wrongly entered."""
    # Checks the list for the channel with the "p_id"
    if p_mode == "ch":
        for channel in p_channel_list:
            if channel.id == p_id:
                return channel  # Returns a Channel object
    elif p_mode == "id":  # This is a verification
        for channel in p_channel_list:
            if channel.id == p_id:
                return channel.id  # Returns the id
    elif p_mode == "na":
        for channel in p_channel_list:
            if channel.id == p_id:
                return channel.name  # Returns the name
    else:
        print("{} MODE DOESN'T EXIST (ObtainChannelInfo)".format(p_mode))
        return "-1"


def obtain_member_info(p_member_list, p_id: str, p_mode="mb", p_server_id=""):
    """Obtains Information from a member.
    
    Keyword arguments:
    p_member_list -- member list
    p_id         -- member.id
    p_mode       -- different mode returns different objects
    p_server_id   -- server id (for 'si' mode)

    Modes:
    mb - Returns a Member (DEFAULT)
    id - Returns a Member.id
    na - Returns a Member.name
    nl - Returns the length of Member.name
    si - Returns a Member.server.id
    Returns -1 and notifies you in console if the mode is wrongly entered."""
    # Checks the list for the member with the "p_id"
    if p_mode == "mb":
        for member in p_member_list:
            if member.id == p_id:
                return member  # Returns a Member object
    elif p_mode == "id":  # This is a verification
        for member in p_member_list:
            if member.id == p_id:
                return member.id  # Returns the id
    elif p_mode == "na":
        for member in p_member_list:
            if member.id == p_id:
                return member.name  # Returns the name
    elif p_mode == "nl":
        for member in p_member_list:
            if member.id == p_id:
                return len(member.name)  # Returns the length of the name
    elif p_mode == "si":  # This is a verification
        for member in p_member_list:
            if member.id == p_id and member.server.id == p_server_id:
                return member.server.id  # Returns the server id of the member.
    else:
        print("{} MODE DOESN'T EXIST (ObtainMemberInfo)".format(p_mode))
        return "-1"


def is_user_id_valid(p_member_list, p_user_id: str):
    """True = Valid
    False = Not valid
    UserId is valid if : It has 18 digits and an existing channel.
    Accepts only digits.

    Keyword arguments:
    p_member_list -- member list
    p_id         -- member.id"""
    return len(p_user_id) == ID_LENGTH and p_user_id == obtain_member_info(p_member_list, p_user_id, "id", "")


def is_channel_id_valid(p_channel_list, p_channel_id: str):
    """True = Valid
    False = Not valid
    ChannelId is valid if : It has 18 digits and an existing member.
    Accepts only digits.

    Keyword arguments:
    p_channel_list -- channel list
    p_channel_id   -- channel.id"""
    if len(p_channel_id) == ID_LENGTH and p_channel_id == obtain_channel_info(p_channel_list, p_channel_id, "id"):
        return True
    return False


def is_admin_user(p_admin_user_list, p_user_id: str):
    """Verifies if the userId is an admin.

    Keyword arguments:
    p_admin_user_list -- admin user list
    p_user_id        -- user id"""
    for adminUser in p_admin_user_list:
        if adminUser == p_user_id:
            return True
    return False


def is_me(p_user_id: str):
    """Verifies if the userId is an admin.

    Keyword arguments:
    p_user_id -- user id"""
    if p_user_id == my_id():
        return True
    return False


def extract_info(p_client, p_wcommand):
    """Fills up every member list.

    Keyword arguments:
    p_client   -- main discord.Client()
    p_wcommand --  main WCommand()"""
    m_NormalMessage.append(p_wcommand.normal_message())
    m_AdminMessage.append(p_wcommand.admin_message())
    m_OwnerMessage.append(p_wcommand.owner_message())

    for server in p_client.servers:
        m_ServerList.append(server)  # Gets every Server

    jsonCollection.file_extract_user_bd(m_UserBDList)  # Gets every UserBd from FileNameUserBD()
    jsonCollection.file_extract_channel_bd(m_ChannelBDList)  # Gets every ChannelBd from FileNameChannelBD()
    jsonCollection.file_extract_admin_user(m_AdminUserList)  # Gets every AdminUser from FileNameAdminUser()
    print(JSON_COLLECTION_MESSAGE)
