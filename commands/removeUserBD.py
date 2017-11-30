from util import *
from cmdtemplate import Command

class removeUserBD(Command):
    """Removes a user from my birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
       return MORE_HELP_REMOVE_USER_BD.format(self.__str__())

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


        userId = str(p_message.author.id)
        listIndex = 0
        for userBd in m_UserBDList:
            if userBd.userId == userId:
                jsonCollection.FileRemoveUserBD(m_UserBDList, listIndex)
                await self.client.send_message(p_message.channel, REMOVE_USER_BD_SUCCESS)
                return
            listIndex += 1
        await self.client.send_message(p_message.channel, REMOVE_USER_BD_NOT_IN)
