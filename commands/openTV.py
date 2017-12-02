import asyncio
import platform

from subprocess import Popen

from util import *
from cmdtemplate import Command


class Opentv(Command):
    """Opens TeamViewer and closes it after {0} seconds."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER
    cmdDoc = SECONDS_TV

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_OPEN_TV.format(self.__str__())

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

        if platform.system() == 'Windows':
            proc = Popen(windows_cmd_open_tv(), shell=True)  # Opens TeamViewer.exe
            await self.client.send_message(p_message.channel, OPEN_TV_OPENING.format(SECONDS_TV))
            await asyncio.sleep(SECONDS_TV)
            proc.kill()  # Closes TeamViewer.exe
            # await client.send_message(p_message.channel, "Closing TeamViewer...")
            return

        if platform.system() == 'Linux':
            proc = Popen(linux_cmd_open_tv(), shell=True)
            await self.client.send_message(p_message.channel, OPEN_TV_OPENING.format(SECONDS_TV))
            await asyncio.sleep(SECONDS_TV)
            proc.kill()
            # await client.send_message(p_message.channel, "Closing TeamViewer...")
            return

        await self.client.send_message(p_message.channel, OPEN_TV_ERROR)
