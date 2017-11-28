from util import *
from cmdtemplate import Command

class town(Command):
    """Population of the town. Woh's Server only."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [anything/anyone]"

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
        return MORE_HELP_TOWN.format(self.__str__(), self.cmdArguments)

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


        if p_message.server.id == MyServer():
            population = self._remCmd(p_message, self.__str__())
            if len(population) != 0:
                await self.client.send_message(p_message.channel, TOWN_STFUT.format(population))
                await self.client.delete_message(p_message)
