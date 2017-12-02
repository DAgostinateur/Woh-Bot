from util import *
from cmdtemplate import Command


class React(Command):
    """React with an emoji from my Emoji Server."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL
    cmdArguments = " [name_of_emoji] [message_id]"

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_REACT.format(self.__str__(), self.cmdArguments)

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        cmd_content = self._rem_cmd(p_message, self.__str__()).split()
        if len(cmd_content) != 2:
            await self.client.delete_message(p_message)
            return

        emoji_name = cmd_content[0]
        msg_id = cmd_content[1]

        try:
            emoji = obtain_emoji_with_name(self.client.get_all_emojis(), emoji_name)
        except EmojiNameNonExistent:
            await self.client.delete_message(p_message)
            return

        try:
            react_message = await self.client.get_message(p_message.channel, msg_id)
        except discord.NotFound:
            await self.client.delete_message(p_message)
            return

        await self.client.add_reaction(react_message, emoji)
        await self.client.delete_message(p_message)
