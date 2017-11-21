from util import *
from cmdtemplate import Command

class listAdminUser(Command):
    """Lists every admin user."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER

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


        serverId = str(p_message.server.id)
        if len(m_AdminUserList) != 0:
            comboList = []
            for adminUser in m_AdminUserList:
                if serverId == ObtainMemberInfo(m_MemberList, adminUser, "si", serverId):
                    name = ObtainMemberInfo(m_MemberList, adminUser, "na", "")
                    comboList.append([name])
                if len(comboList) == 10:
                    fullMessage = CodeFormat(tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                    await self.client.send_message(p_message.author, fullMessage)
                    del comboList
            if len(comboList) != 0 or comboList is not None:
                fullMessage = CodeFormat(tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                await self.client.send_message(p_message.author, fullMessage)
        else: 
            await self.client.send_message(p_message.author, "The list is empty.")
