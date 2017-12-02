from util import *
from cmdtemplate import Command


class Showchannelbd(Command):
    """Shows the current channel used for birthday messages."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_SHOW_CHANNEL_BD.format(self.__str__())

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        for channelBD in m_ChannelBDList:
            if channelBD.serverId == str(p_message.server.id):
                msg = SHOW_CHANNEL_BD_SEND_IN.format(channel_format(channelBD.channelId))
                await self.client.send_message(p_message.channel, msg)
                return
        await self.client.send_message(p_message.channel, SHOW_CHANNEL_BD_NONE)
