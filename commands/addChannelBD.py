from util import *
from cmdtemplate import Command

class addChannelBD(Command):
    """Shows the current channel used for birthday messages."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN
    cmdArguments = " [channel]"

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


        channelId = self._remCmd(p_message, self.__str__)
        channelId = search("[0-9]{18}", channelId).group()
        if not IsChannelIdValid(m_ChannelList, channelId):
            await self.client.send_message(p_message.channel, "**Invalid channel**, make sure you entered a real channel from this server.")
            return
            
        for channelBD in m_ChannelBDList:
            if channelBD.channelId == channelId:
                msg = "**There's already a channel for birthday messages in this server**, delete the current one to change it."
                await self.client.send_message(p_message.channel, msg)
                return

        await self.client.send_message(p_message.channel, "I will now send birthday messages in {}.".format(ChannelFormat(channelId)))
        FileAddChannelBD(m_ChannelBDList, channelId, str(p_message.server.id))
