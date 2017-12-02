from util import *
from cmdtemplate import Command


class Removechannelbd(Command):
    """Unset the channel for birthday messages."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_REMOVE_CHANNEL_BD.format(self.__str__())

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

        list_index = 0
        for channelBD in m_ChannelBDList:
            if channelBD.serverId == p_message.server.id:
                file_remove_channel_bd(m_ChannelBDList, list_index)
                await self.client.send_message(p_message.channel, REMOVE_CHANNEL_BD_SUCCESS)
                return
            list_index += 1
        await self.client.send_message(p_message.channel, REMOVE_CHANNEL_BD_EMPTY)
