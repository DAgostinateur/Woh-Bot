from util import *
from cmdtemplate import Command

class setPresence(Command):
    """Sets the bot's presence."""

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


        gameName = self._remCmd(p_message, self.__str__)
        if len(gameName) != 0:
            game = discord.Game(name="{0}".format(gameName))
            await self.client.change_presence(game=game)
            await self.client.send_message(p_message.channel, "Changed Presence!")
