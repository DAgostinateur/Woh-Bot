from util import *

class Command():
    """A command template"""

    isDisabled = True # Is the command disabled
    permissionLevel = PERM_LEVEL_NONE
    cmdArguments = ""
    cmdDoc = ""

    def __init__(self, client):
        if False:
            client = discord.Client()
        self.client = client

    def _getCmd(self, p_message, p_cmdName):
        """Returns the command from a
        message's content.
        
        Keyword arguments:
        p_message -- a Discord message
        p_cmdName -- function name/command name"""
        msg = p_message.content[:len("{0}{1}".format(PREFIX, p_cmdName))]
        return msg

    def _remCmd(self, p_message, p_cmdName):
        """Returns the content of a message
        without the start of the command.
        
        Keyword arguments:
        p_message -- a Discord message
        p_cmdName -- function name/command name"""
        return p_message.content[len("{0}{1}".format(PREFIX, p_cmdName)):].lstrip()

    def cmdCalled(self, p_message, p_cmdName):
        """Returns True if the message's command
        is equivalent to a command name, ignoring
        character case.
        Returns False otherwise.
        
        Keyword arguments:
        p_message -- a Discord message
        p_cmdName -- function name/command name"""
        msgCmd = self._getCmd(p_message, p_cmdName)
        cmd = "{0}{1}".format(PREFIX, p_cmdName)
        if msgCmd.lower() == cmd.lower():
            return True
        return False

    def hasPermission(self, permissions, userId):
        """Returns True if the user has
        permission to use the command.
        Returns False otherwise.

        Keyword arguments:
        permissions -- permission level
        userId      -- a user id
        
        Permission Levels:
        normal - Everyone has access
        admin  - Admins and I has access
        owner  - Only I have access"""
        if permissions == PERM_LEVEL_NORMAL:
            return True
        elif permissions == PERM_LEVEL_ADMIN:
            if IsAdminUser(m_AdminUserList, userId) or IsMe(userId):
                return True
        elif permissions == PERM_LEVEL_OWNER:
            if IsMe(userId):
                return True
        else:
            return False
        return False
