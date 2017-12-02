from util import *
from cmdtemplate import Command


class Setpresence(Command):
    """Sets the bot's presence."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER
    cmdArguments = " [game]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_SET_PRESENCE.format(self.__str__(), self.cmdArguments)

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

        game_name = self._rem_cmd(p_message, self.__str__())
        if len(game_name) != 0:
            game = discord.Game(name="{0}".format(game_name))
            await self.client.change_presence(game=game)
            await self.client.send_message(p_message.channel, SET_PRESENCE_CHANGE)
