from util import *
from cmdtemplate import Command

class woh(Command):
    """Sends you the list of commands."""

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

        await self.client.send_message(p_message.author, m_NormalMessage[0])
        if IsAdminUser(m_AdminUserList, p_message.author.id) or IsMe(p_message.author.id):
            await self.client.send_message(p_message.author, m_AdminMessage[0])

        if IsMe(p_message.author.id):
            await self.client.send_message(p_message.author, m_OwnerMessage[0])
