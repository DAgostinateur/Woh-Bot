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

    async def command(self, p_message):
        """Actual Command"""
        if self.isDisabled:
            return

        if not self.cmdCalled(p_message, self.__str__()):
            return

        if not self.hasPermission(self.permissionLevel, p_message.author.id):
            return


        userId = str(p_message.author.id)
        listIndex = 0 # Will be sent to FileRemoveUserBD
        for userBd in m_UserBDList:
            if userBd.userId == userId:
                FileRemoveUserBD(m_UserBDList, listIndex)
                await self.client.send_message(p_message.channel, "You are no longer in my birthday list.")
                return
            listIndex += 1
        await self.client.send_message(p_message.channel, "Can't remove you if you're not in my list.")
