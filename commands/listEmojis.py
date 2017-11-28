from util import *
from cmdtemplate import Command

class listEmojis(Command):
    """Lists every emoji Woh Bot has access to."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
       return "Command: {0}\nWhen the command is called, the bot will send you the list of **custom emojis** that is has access to.\nThese custom emojis are from every server Woh Bot is in.\nIt will use this format [Name] [Emoji]".format(self.__str__())

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


        # The emoji list should never be empty
        # If it was, Woh Bot would be in 0 servers
        head  = ["Name", "Emoji"]
        comboList = []
        for emoji in self.client.get_all_emojis():
            comboList.append([emoji.name, str(emoji)])
            if len(comboList) == 30:
                fullMessage = tabulate.tabulate(comboList, headers=head, tablefmt="simple")
                await self.client.send_message(p_message.author, fullMessage)
                del comboList[:]
        if len(comboList) != 0 or comboList is not None:
            fullMessage = tabulate.tabulate(comboList, headers=head, tablefmt="simple")
            await self.client.send_message(p_message.author, fullMessage)