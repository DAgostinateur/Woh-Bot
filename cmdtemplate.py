from util import *


class Command:
    """A command template"""

    isDisabled = True  # Is the command disabled
    permissionLevel = PERM_LEVEL_NONE
    cmdArguments = ""
    cmdDoc = ""

    def more_help(self):
        return MORE_HELP_DEFAULT

    def __init__(self, client):
        if False:
            client = discord.Client()
        self.client = client

    @staticmethod
    def _get_cmd(p_message, p_cmd_name):
        """Returns the command from a
        message's content.
        
        Keyword arguments:
        p_message -- a Discord message
        p_cmd_name -- function name/command name"""
        return p_message.content[:len("{0}{1}".format(PREFIX, p_cmd_name))]

    @staticmethod
    def _rem_cmd(p_message, p_cmd_name):
        """Returns the content of a message
        without the start of the command.
        
        Keyword arguments:
        p_message -- a Discord message
        p_cmd_name -- function name/command name"""
        return p_message.content[len("{0}{1}".format(PREFIX, p_cmd_name)):].lstrip()

    def cmd_called(self, p_message, p_cmd_name):
        """Returns True if the message's command
        is equivalent to a command name, ignoring
        character case.
        Returns False otherwise.
        
        Keyword arguments:
        p_message -- a Discord message
        p_cmd_name -- function name/command name"""
        msg_cmd = self._get_cmd(p_message, p_cmd_name)
        cmd = "{0}{1}".format(PREFIX, p_cmd_name)
        if msg_cmd.lower() == cmd.lower():
            return True
        return False

    @staticmethod
    def has_permission(permissions, user_id):
        """Returns True if the user has
        permission to use the command.
        Returns False otherwise.

        Keyword arguments:
        permissions -- permission level
        user_id      -- a user id

        Permission Levels:
        normal - Everyone has access
        admin  - Admins and I have access
        owner  - Only I have access"""
        if permissions == PERM_LEVEL_NORMAL:
            return True
        elif permissions == PERM_LEVEL_ADMIN:
            if is_admin_user(m_AdminUserList, user_id) or is_me(user_id):
                return True
        elif permissions == PERM_LEVEL_OWNER:
            if is_me(user_id):
                return True
        else:
            return False
        return False

    async def execute_command(self, p_is_disabled, p_message, p_cmd_name, p_permission_level, p_more_help):
        if p_is_disabled:
            return True

        if not self.cmd_called(p_message, p_cmd_name):
            return True

        if not self.has_permission(p_permission_level, p_message.author.id):
            return True

        if HELP_COMMAND_PREFIX in p_message.content.lower():
            await self.client.send_message(p_message.author, p_more_help)
            return True

        return False
