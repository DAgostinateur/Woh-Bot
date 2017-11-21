from util import *
from cmdtemplate import Command

class removeChannelBD(Command):
    """Unsets the channel for birthday messages."""

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


        listIndex = 0 # Will be sent to FileRemoveChannelBD
        for channelBD in m_ChannelBDList:
            if channelBD.serverId == p_message.server.id:
                FileRemoveChannelBD(m_ChannelBDList, listIndex)
                await self.client.send_message(p_message.channel, "I will no longer send birthday messages in this server.")
                return
            listIndex += 1
        await self.client.send_message(p_message.channel, "There's no channel to remove.")
