from re import search

from util import *
from cmdtemplate import Command


class Addchannelbd(Command):
    """Sets the channel used for birthday messages."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN
    cmdArguments = " [channel]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_ADD_CHANNEL_BD.format(self.__str__(), self.cmdArguments)

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

        channel_id = self._rem_cmd(p_message, self.__str__())
        channel_id = search(ID_REGEX, channel_id).group()
        if not is_channel_id_valid(self.client.get_all_channels(), channel_id):
            await self.client.send_message(p_message.channel, INVALID_CHANNEL)
            return

        for channelBD in m_ChannelBDList:
            if channelBD.channelId == channel_id:
                await self.client.send_message(p_message.channel, ADD_CHANNEL_BD_ALREADY)
                return

        await self.client.send_message(p_message.channel, ADD_CHANNEL_BD_SUCCESS.format(channel_format(channel_id)))
        file_add_channel_bd(m_ChannelBDList, channel_id, str(p_message.server.id))
