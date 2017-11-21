from util import *
from cmdtemplate import Command

class addAdminUser(Command):
    """Adds an admin user."""

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


        userId = self._remCmd(p_message, self.__str__)
        userId = search("[0-9]{18}", userId).group()
        if not IsUserIdValid(self.client.get_all_members(), userId):
            await self.client.send_message(p_message.channel, "**Invalid user**, make sure you entered a real user from this server.")
            return

        for adminUser in m_AdminUserList:
            if ObtainMemberInfo(self.client.get_all_members(), userId, "id", "") == adminUser:
                await self.client.send_message(p_message.channel, "The user is already an admin.")
                return
                
        await self.client.send_message(p_message.channel, "Admin Added.".format(UserFormat(userId)))
        FileAddAdminUser(m_AdminUserList, userId)
