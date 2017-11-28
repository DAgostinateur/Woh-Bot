from util import *
from cmdtemplate import Command

class react(Command):
    """React with an emoji from my Emoji Server."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [name_of_emoji] [message_id]"

    def getDoc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def moreHelp(self):
       return MORE_HELP_REACT.format(self.__str__(), self.cmdArguments)

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


        cmdContent = self._remCmd(p_message, self.__str__()).split()
        if len(cmdContent) != 2:
            await self.client.delete_message(p_message)
            return

        emojiName = cmdContent[0]
        msgId = cmdContent[1]
        emoji = object()
        reactMessage = object()

        try:
            emoji = ObtainEmojiWithName(self.client.get_all_emojis(), emojiName)
        except Exception:
            await self.client.delete_message(p_message)
            return

        try:
            reactMessage = await self.client.get_message(p_message.channel, msgId)
        except Exception:
            await self.client.delete_message(p_message)
            return

        await self.client.add_reaction(reactMessage, emoji)
        await self.client.delete_message(p_message)