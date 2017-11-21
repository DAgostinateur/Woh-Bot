from util import *
from cmdtemplate import Command

class listAllUserBD(Command):
    """Lists the entire birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN

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


        if len(m_UserBDList) != 0:
            head = ["Name", "Birthday(mm-dd)", "User ID"]
            comboList = []
            for userBd in m_UserBDList:
                member = ObtainMemberInfo(self.client.get_all_members(), userBd.userId, "mb", "")
                comboList.append([member.name, userBd.bd, member.id])
                if len(comboList) == 10:
                    fullMessage = CodeFormat(tabulate(comboList, headers=head, tablefmt="fancy_grid"), "")
                    await self.client.send_message(p_message.author, fullMessage)
                    del comboList
            if len(comboList) != 0 or comboList is not None:
                fullMessage = CodeFormat(tabulate(comboList, headers=head, tablefmt="fancy_grid"), "")
                await self.client.send_message(p_message.author, fullMessage)
        else: 
            await self.client.send_message(p_message.author, "The list is empty.")
