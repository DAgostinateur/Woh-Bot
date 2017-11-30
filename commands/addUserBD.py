from util import *
from cmdtemplate import Command

class addUserBD(Command):
    """Adds you to my birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [mm-dd]"

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
       return MORE_HELP_ADD_USER_BD.format(self.__str__(), self.cmdArguments)

    async def command(self, p_message):
        """Actual Command"""
        if self.isDisabled:
            return

        if not self.cmdCalled(p_message, self.__str__()):
            return

        if not self.hasPermission(self.permissionLevel, p_message.author.id):
            return

        if HELP_COMMAND_PREFIX in p_message.content.lower():
            await self.client.send_message(p_message.author, self.moreHelp())
            return


        for userBd in m_UserBDList:
            if ObtainMemberInfo(self.client.get_all_members(), str(p_message.author.id), "id", "") == userBd.userId:
                await self.client.send_message(p_message.channel, ADD_USER_BD_ALREADY)
                return
        bd = self._remCmd(p_message, self.__str__())
        userId = str(p_message.author.id)

        try:
            bdTest = datetime.strptime(bd, "%m-%d") # Verifying the date
        except ValueError:
            await self.client.send_message(p_message.channel, INVALID_DATE)
            return

        jsonCollection.FileAddUserBD(m_UserBDList, userId, bd)
        await self.client.send_message(p_message.channel, ADD_USER_BD_SUCCESS)
