from util import *
from cmdtemplate import Command


class openTV(Command):
    """Opens TeamViewer and closes it after {0} seconds."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_OWNER
    cmdDoc = SECONDS_TV

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
       return "Command: {0}\nWhen the command is called, the bot will open Teamviewer on the host PC and close it after x seconds.\nClosing doesn't actually work, meaning it's a one time use command.".format(self.__str__())

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


        if platform.system() == 'Windows':
            proc = Popen(WindowsCmdOpenTV(), shell=True) # Opens TeamViewer.exe
            await self.client.send_message(p_message.channel, "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds.".format(SECONDS_TV))
            await asyncio.sleep(SECONDS_TV)
            proc.kill() # Closes TeamViewer.exe
            #await client.send_message(p_message.channel, "Closing TeamViewer...")
            return

        if platform.system() == 'Linux':
            proc = Popen(LinuxCmdOpenTV(), shell=True)
            await self.client.send_message(p_message.channel, "Opening TeamViewer...\nTeamViewer will maybe close in {0} seconds.".format(SECONDS_TV))
            await asyncio.sleep(SECONDS_TV)
            proc.kill()
            #await client.send_message(p_message.channel, "Closing TeamViewer...")
            return

        await self.client.send_message(p_message.channel, "**ERROR, host PC is not a Windows or Linux OS**")
