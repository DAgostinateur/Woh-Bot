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

    def moreHelp(self):
       return "Command: {0}\nWhen the command is called, the bot will send you the entire list of user's birthday.\nIt will use this format [Name] [Birthday(mm-dd)] [UserId]".format(self.__str__())

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


        if len(m_UserBDList) != 0:
            head = ["Name", "Birthday(mm-dd)", "User ID"]
            comboList = []
            for userBd in m_UserBDList:
                member = ObtainMemberInfo(self.client.get_all_members(), userBd.userId, "mb", "")
                comboList.append([member.name, userBd.bd, member.id])
                if len(comboList) == 10:
                    fullMessage = CodeFormat(tabulate.tabulate(comboList, headers=head, tablefmt="fancy_grid"), "")
                    await self.client.send_message(p_message.author, fullMessage)
                    del comboList[:]
            if len(comboList) != 0 or comboList is not None:
                fullMessage = CodeFormat(tabulate.tabulate(comboList, headers=head, tablefmt="fancy_grid"), "")
                await self.client.send_message(p_message.author, fullMessage)
        else: 
            await self.client.send_message(p_message.author, "The list is empty.")
