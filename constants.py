HELP_COMMAND_PREFIX = "--help"  # The parameter used to get more information about a command
PREFIX = '!'  # The prefix used for commands
ID_LENGTH = 18  # Length of a Discord Id
SECONDS_TV = 600  # Number of seconds before closing TeamViewer

# Permissions for commands:
PERM_LEVEL_NONE = 0  # Command access: Nobody
PERM_LEVEL_NORMAL = 1  # Command access: Everyone
PERM_LEVEL_ADMIN = 2  # Command access: Admin Users (made admin by me) and me
PERM_LEVEL_OWNER = 3  # Command access: Me

# Message will appear on the console on startup:
CONSOLE_MESSAGE = "-----------\nWoh Bot\n-----------\nLogged in as {0}\nCreator : D'Agostinateur Woh\n-----------"

# Message will appear after the collection of lists is done:
JSON_COLLECTION_MESSAGE = "List of Servers collected.\nList of UserBD collected.\nList of ChannelBD collected.\nList " \
                          "of AdminUser collected. "

# Messages to indicate an important change(this will only appear on console):
ADMIN_USER_REMOVED_STRING = "AdminUser List updated. AdminUser removed."
ADMIN_USER_ADDED_STRING = "AdminUser List updated. AdminUser added."
CHANNEL_BD_REMOVED_STRING = "ChannelBD List updated. ChannelBD removed."
CHANNEL_BD_ADDED_STRING = "ChannelBD List updated. ChannelBD added."
USER_BD_REMOVED_STRING = "UserBD List updated. UserBD removed."
USER_BD_ADDED_STRING = "UserBD List updated. UserBD added."

# Text at the beginning of each help message:
NORMAL_MESSAGE_START = "My prefix is [{0}]. {0}[command_name] --help for more information. SORRY MOBILE USERS\n"
ADMIN_MESSAGE_START = "Admin commands.\n"
OWNER_MESSAGE_START = "Owner commands.\n"

HAPPY_BIRTHDAY_START = "{0} Happy Birthday "  # Actual happy birthday message

# Default moreHelp() text:
MORE_HELP_DEFAULT = "No documentation for this command. Please notify the owner."

#############################
# Every command's constants #
#############################
INVALID_USER = "**Invalid user**, make sure you entered a real user from this server."
INVALID_DATE = "**Invalid date**, make sure you entered a possible date."
INVALID_CHANNEL = "**Invalid channel**, make sure you entered a real channel from this server."
ID_REGEX = "[0-9]{18}"
EMPTY_LIST = "The list is empty."

# addAdminUser:
ADD_ADMIN_USER_ALREADY = "The user is already an admin."
ADD_ADMIN_USER_SUCCESS = "{0} now has access to admin commands."
# addChannelBD:
ADD_CHANNEL_BD_INVALID = ""
ADD_CHANNEL_BD_ALREADY = "**There's already a channel for birthday messages in this server**, delete the current one " \
                         "to change it. "
ADD_CHANNEL_BD_SUCCESS = "I will now send birthday messages in {0}."
# addUserBD:
ADD_USER_BD_ALREADY = "You're already in my list"
ADD_USER_BD_SUCCESS = "Added birthday."
# city:
CITY_GC = "Gotem City\nPopulation: {0}"  # Inside joke format
# listAdminUser:
# listAllUserBD:
# listEmojis:
# listUserBD:
# openTV:
OPEN_TV_OPENING = "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds."
OPEN_TV_ERROR = "**ERROR, host PC is not a Windows or Linux OS**"
# react:
# removeAdminUser:
REMOVE_ADMIN_USER_SUCCESS = "{0} is no longer an admin."
REMOVE_ADMIN_USER_NOT_IN = "Can't remove the user if he's not in the list."
# removeChannelBD:
REMOVE_CHANNEL_BD_EMPTY = "There's no channel to remove."
REMOVE_CHANNEL_BD_SUCCESS = "I will no longer send birthday messages in this server."
# removeUserBD:
REMOVE_USER_BD_SUCCESS = "You are no longer in my birthday list."
REMOVE_USER_BD_NOT_IN = "Can't remove you if you're not in my list."
# setPresence:
SET_PRESENCE_CHANGE = "Changed Presence!"  # Message to confirm the change
# showChannelBD:
SHOW_CHANNEL_BD_NONE = "I don't send birthday messages in this server."  # When there's no channels used on the server
SHOW_CHANNEL_BD_SEND_IN = "I send birthday messages to {0}."  # Showing the channel used
# town:
TOWN_STFUT = "Shut the Fuck Up Town\nPopulation: {0}"  # Inside joke format
# woh:


##############################
# Every command's moreHelp() #
##############################
# addAdminUser:
MORE_HELP_ADD_ADMIN_USER = "Command: {0}{1}\nWhen the command is called, the bot will grant a user permission to use " \
                           "admin commands. "
# addChannelBD:
MORE_HELP_ADD_CHANNEL_BD = "Command: {0}{1}\nWhen the command is called, the bot will set the channel used for " \
                           "sending birthday wishes. "
# addUserBD:
MORE_HELP_ADD_USER_BD = "Command: {0}{1}\nWhen the command is called, the bot will add the user in its birthday " \
                        "list.\nThe person will now receive birthday wishes on its birthday.\nHere's an example of a " \
                        "[mm-dd] format: 03-05 , which means March 5th. "
# city:
MORE_HELP_CITY = "Command: {0}{1}\nWhen the command is called, the bot will put the user input in the Gotem City " \
                 "format.\n_This is an inside joke_. Woh's Server only. "
# listAdminUser:
MORE_HELP_LIST_ADMIN_USER = "Command: {0}\nWhen the command is called, the bot will send you the list of users that " \
                            "have access to admin commands.\nIt will use this format [Name]. "
# listAllUserBD:
MORE_HELP_LIST_ALL_USER_BD = "Command: {0}\nWhen the command is called, the bot will send you the entire list of " \
                             "user's birthday.\nIt will use this format [Name] [Birthday(mm-dd)] [UserId]. "
# listEmojis:
MORE_HELP_LIST_EMOJIS = "Command: {0}\nWhen the command is called, the bot will send you the list of **custom " \
                        "emojis** that is has access to.\nThese custom emojis are from every server Woh Bot is " \
                        "in.\nIt will use this format [Name] [Emoji]. "
# listUserBD:
MORE_HELP_LIST_USER_BD = "Command: {0}\nWhen the command is called, the bot will send you the list of " \
                         "user's birthday from this server.\nIt will use this format [Name] [Birthday(mm-dd)]. "
# openTV:
MORE_HELP_OPEN_TV = "Command: {0}\nWhen the command is called, the bot will open Teamviewer on the host PC and close " \
                    "it after x seconds.\nClosing doesn't actually work, meaning it's a one time use command. "
# react:
MORE_HELP_REACT = "Command: {0}{1}\nWhen the command is called, the bot will add a reaction to a message.\nThis is " \
                  "very useful if you want to use ***custom*** emojis from other servers where Woh Bot is in.\nYou " \
                  "can get message ids only on pc, by enabling Developer Mode in the settings and right clicking a " \
                  "message. "
# removeAdminUser:
MORE_HELP_REMOVE_ADMIN_USER = "Command: {0}{1}\nWhen the command is called, the bot will remove a user's permission " \
                              "to use admin commands. "
# removeChannelBD:
MORE_HELP_REMOVE_CHANNEL_BD = "Command: {0}\nWhen the command is called, the bot will remove the channel used for " \
                              "sending birthday wishes.\nRemoving the channel doesn't actually delete the channel, " \
                              "it just stops the bot from sending birthday wishes. "
# removeUserBD:
MORE_HELP_REMOVE_USER_BD = "Command: {0}\nWhen the command is called, the bot will remove the user from its birthday " \
                           "list, meaning it stops sending birthday wishes to that person. "
# setPresence:
MORE_HELP_SET_PRESENCE = "Command: {0}{1}\nWhen the command is called, the bot will change it's playing status with " \
                         "user input. **Doesn't work** "
# showChannelBD:
MORE_HELP_SHOW_CHANNEL_BD = "Command: {0}\nWhen the command is called, the bot will send the current channel" \
                            " used for sending birthday wishes. "
# town:
MORE_HELP_TOWN = "Command: {0}{1}\nWhen the command is called, the bot will put the user input in the Shut The Fuck " \
                 "Up Town format.\n_This is an inside joke_. Woh's Server only. "
# woh:
MORE_HELP_WOH = "Command: {0}\nWhen the command is called, the bot will send you the list of commands that you have " \
                "permission to use. "
