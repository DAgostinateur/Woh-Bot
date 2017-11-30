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

    def moreHelp(self):
       return MORE_HELP_REMOVE_CHANNEL_BD.format(self.__str__())

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


        listIndex = 0
        for channelBD in m_ChannelBDList:
            if channelBD.serverId == p_message.server.id:
                jsonCollection.FileRemoveChannelBD(m_ChannelBDList, listIndex)
                await self.client.send_message(p_message.channel, REMOVE_CHANNEL_BD_SUCCESS)
                return
            listIndex += 1
        await self.client.send_message(p_message.channel, REMOVE_CHANNEL_BD_EMPTY)
