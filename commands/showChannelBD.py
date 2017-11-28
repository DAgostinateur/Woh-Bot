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

    def moreHelp(self):
        return MORE_HELP_SHOW_CHANNEL_BD.format(self.__str__())

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


        for channelBD in m_ChannelBDList:
            if channelBD.serverId == str(p_message.server.id):
                msg = SHOW_CHANNEL_BD_SEND_IN.format(ChannelFormat(channelBD.channelId))
                await self.client.send_message(p_message.channel, msg)
                return
        await self.client.send_message(p_message.channel, SHOW_CHANNEL_BD_NONE)
