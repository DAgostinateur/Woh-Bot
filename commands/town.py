from util import *
from cmdtemplate import Command


class Town(Command):
    """Population of the town. Woh's Server only."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [anything/anyone]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_TOWN.format(self.__str__(), self.cmdArguments)

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        if p_message.server.id == my_server():
            population = self._rem_cmd(p_message, self.__str__())
            if len(population) != 0:
                await self.client.send_message(p_message.channel, TOWN_STFUT.format(population))
                await self.client.delete_message(p_message)
