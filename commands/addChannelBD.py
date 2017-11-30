from util import *
from cmdtemplate import Command

class addChannelBD(Command):
    """Sets the channel used for birthday messages."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN
    cmdArguments = " [channel]"

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
       return MORE_HELP_ADD_CHANNEL_BD.format(self.__str__(), self.cmdArguments)

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


        channelId = self._remCmd(p_message, self.__str__())
        channelId = search(ID_REGEX, channelId).group()
        if not IsChannelIdValid(self.client.get_all_channels(), channelId):
            await self.client.send_message(p_message.channel, INVALID_CHANNEL)
            return
            
        for channelBD in m_ChannelBDList:
            if channelBD.channelId == channelId:
                await self.client.send_message(p_message.channel, ADD_CHANNEL_BD_ALREADY)
                return

        await self.client.send_message(p_message.channel, ADD_CHANNEL_BD_SUCCESS.format(ChannelFormat(channelId)))
        jsonCollection.FileAddChannelBD(m_ChannelBDList, channelId, str(p_message.server.id))
