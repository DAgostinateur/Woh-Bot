from util import *
from cmdtemplate import Command

class showChannelBD(Command):
    """Shows the current channel used for birthday messages."""

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


        for channelBD in m_ChannelBDList:
            if channelBD.serverId == str(p_message.server.id):
                msg = "I send birthday messages to {}.".format(ChannelFormat(channelBD.channelId))
                await self.client.send_message(p_message.channel, msg)
                return
        await self.client.send_message(p_message.channel, "I don't send birthday messages in this server.")
