from util import *
from cmdtemplate import Command

class listUserBD(Command):
    """Lists everyone from my birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
        return "Command: {0}\nWhen the command is called, the bot will send you the list of user's birthday from this server.\nIt will use this format [Name] [Birthday(mm-dd)]".format(self.__str__())

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
        if len(m_UserBDList) != 0:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == serverId:
                    comboList = []
                    for userBd in m_UserBDList:
                        if serverId == ObtainMemberInfo(self.client.get_all_members(), userBd.userId, "si", serverId):
                            name = ObtainMemberInfo(self.client.get_all_members(), userBd.userId, "na", "")
                            comboList.append([name, userBd.bd])
                        if len(comboList) == 10:
                            fullMessage = CodeFormat(tabulate.tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"), "")
                            await self.client.send_message(p_message.author, fullMessage)
                            del comboList[:]
                    if len(comboList) != 0 or comboList is not None:
                        fullMessage = CodeFormat(tabulate.tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"), "")
                        await self.client.send_message(p_message.author, fullMessage)
        else: 
            await self.client.send_message(p_message.author, "The list is empty.")
