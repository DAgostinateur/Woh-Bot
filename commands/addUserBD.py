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

    async def command(self, p_message):
        """Actual Command"""
        if self.isDisabled:
            return

        if not self.cmdCalled(p_message, self.__str__()):
            return

        if not self.hasPermission(self.permissionLevel, p_message.author.id):
            return


        for userBd in m_UserBDList:
            if ObtainMemberInfo(m_MemberList, str(p_message.author.id), "id", "") == userBd.userId:
                await self.client.send_message(p_message.channel, "You're already in my list")
                return
        bd = self._remCmd(p_message, self.__str__)
        userId = str(p_message.author.id)

        try:
            bdTest = datetime.strptime(bd, "%m-%d") # Verifying the date
        except ValueError:
            await self.client.send_message(p_message.channel, "**Invalid date**, make sure you entered a possible date.")
            return

        if not IsUserIdValid(m_MemberList, userId): # Supposed to always return true
            await client.send_message(p_message.channel, "**You're not in my list of Members**")
            return

        FileAddUserBD(m_UserBDList, userId, bd)
        await self.client.send_message(p_message.channel, "Added birthday.")
