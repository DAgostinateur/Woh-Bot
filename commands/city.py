from util import *
from cmdtemplate import Command


class City(Command):
    """Population of the city. Woh's Server only."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [anything/anyone]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_CITY.format(self.__str__(), self.cmdArguments)

    async def command(self, p_message):
        """Actual Command"""
        if self.isDisabled:
            return

        if not self.cmd_called(p_message, self.__str__()):
            return

        if not self.has_permission(self.permissionLevel, p_message.author.id):
            return

        if HELP_COMMAND_PREFIX in p_message.content.lower():
            await self.client.send_message(p_message.author, self.more_help())
            return

        if p_message.server.id == my_server():
            population = self._rem_cmd(p_message, self.__str__())
            if len(population) != 0:
                await self.client.send_message(p_message.channel, CITY_GC.format(population))
                await self.client.delete_message(p_message)
