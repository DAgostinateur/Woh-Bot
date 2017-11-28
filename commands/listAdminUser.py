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

    def moreHelp(self):
       return "Command: {0}\nWhen the command is called, the bot will send you the list of users that have access to admin commands.\nIt will use this format [Name]".format(self.__str__())

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


        serverId = str(p_message.server.id)
        if len(m_AdminUserList) != 0:
            comboList = []
            for adminUser in m_AdminUserList:
                if serverId == ObtainMemberInfo(self.client.get_all_members(), adminUser, "si", serverId):
                    name = ObtainMemberInfo(self.client.get_all_members(), adminUser, "na", "")
                    comboList.append([name])
                if len(comboList) == 10:
                    fullMessage = CodeFormat(tabulate.tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                    await self.client.send_message(p_message.author, fullMessage)
                    del comboList[:]
            if len(comboList) != 0 or comboList is not None:
                fullMessage = CodeFormat(tabulate.tabulate(comboList, headers=["Name"], tablefmt="fancy_grid"), "")
                await self.client.send_message(p_message.author, fullMessage)
        else: 
            await self.client.send_message(p_message.author, "The list is empty.")
