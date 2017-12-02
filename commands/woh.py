from util import *
from cmdtemplate import Command


class Woh(Command):
    """Sends you the list of commands."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_WOH.format(self.__str__())

    async def command(self, p_message):
        """Actual Command"""
        if self.isDisabled:
            return

        if not self.cmd_called(p_message, self.__str__()):
            return

        if not self.has_permission(self.permissionLevel, p_message.author.id):
            return

        if HELP_COMMAND_PREFIX in p_message.content.lower():
            await self.client.send_message(p_message.author, self.more_help())
            return

        await self.client.send_message(p_message.author, m_NormalMessage[0])
        if is_admin_user(m_AdminUserList, p_message.author.id) or is_me(p_message.author.id):
            await self.client.send_message(p_message.author, m_AdminMessage[0])

        if is_me(p_message.author.id):
            await self.client.send_message(p_message.author, m_OwnerMessage[0])
