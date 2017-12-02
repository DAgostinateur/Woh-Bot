from util import *
from cmdtemplate import Command


class Removeuserbd(Command):
    """Removes a user from my birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_REMOVE_USER_BD.format(self.__str__())

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        user_id = str(p_message.author.id)
        list_index = 0
        for userBd in m_UserBDList:
            if userBd.userId == user_id:
                file_remove_user_bd(m_UserBDList, list_index)
                await self.client.send_message(p_message.channel, REMOVE_USER_BD_SUCCESS)
                return
            list_index += 1
        await self.client.send_message(p_message.channel, REMOVE_USER_BD_NOT_IN)
