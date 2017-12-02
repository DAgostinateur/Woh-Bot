from re import search

from util import *
from cmdtemplate import Command


class Addadminuser(Command):
    """Adds an admin user."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER
    cmdArguments = " [user]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_ADD_ADMIN_USER.format(self.__str__(), self.cmdArguments)

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

        user_id = self._rem_cmd(p_message, self.__str__())
        user_id = search(ID_REGEX, user_id).group()
        if not is_user_id_valid(self.client.get_all_members(), user_id):
            await self.client.send_message(p_message.channel, INVALID_USER)
            return

        for adminUser in m_AdminUserList:
            if obtain_member_info(self.client.get_all_members(), user_id, "id", "") == adminUser:
                await self.client.send_message(p_message.channel, ADD_ADMIN_USER_ALREADY)
                return

        await self.client.send_message(p_message.channel, ADD_ADMIN_USER_SUCCESS.format(user_format(user_id)))
        jsonCollection.file_add_admin_user(m_AdminUserList, user_id)
