from util import *
from cmdtemplate import Command

class removeAdminUser(Command):
    """Removes an admin user."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER
    cmdArguments = " [user]"

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


        userId = self._remCmd(p_message, self.__str__())
        userId = re.search("[0-9]{18}", userId).group()
        if not IsUserIdValid(m_MemberList, userId):
            await self.client.send_message(p_message.channel, "**Invalid user**, make sure you entered a real user from this server.")
            return

        listIndex = 0
        for adminUser in m_AdminUserList:
            if ObtainMemberInfo(m_MemberList, userId, "id", "") == adminUser:
                FileRemoveAdminUser(m_AdminUserList, listIndex)
                await self.client.send_message(p_message.channel, "Removed User Admin.")
                return
            listIndex += 1
        await self.client.send_message(p_message.channel, "Can't remove the user if he's not in the list.")