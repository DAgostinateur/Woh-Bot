from util import *
from cmdtemplate import Command


class Adduserbd(Command):
    """Adds you to my birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [mm-dd]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_ADD_USER_BD.format(self.__str__(), self.cmdArguments)

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        for userBd in m_UserBDList:
            if obtain_member_info(self.client.get_all_members(), str(p_message.author.id), "id", "") == userBd.userId:
                await self.client.send_message(p_message.channel, ADD_USER_BD_ALREADY)
                return
        bd = self._rem_cmd(p_message, self.__str__())
        user_id = str(p_message.author.id)

        try:
            bd = str(datetime.strptime(bd, "%m-%d"))  # Verifying the date
        except ValueError:
            await self.client.send_message(p_message.channel, INVALID_DATE)
            return

        file_add_user_bd(m_UserBDList, user_id, bd)
        await self.client.send_message(p_message.channel, ADD_USER_BD_SUCCESS)
