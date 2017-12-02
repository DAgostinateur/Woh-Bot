from util import *
from cmdtemplate import Command


class Listemojis(Command):
    """Lists every emoji Woh Bot has access to."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_LIST_EMOJIS.format(self.__str__())

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

        # The emoji list should never be empty
        # If it was, Woh Bot would be in 0 servers
        head = ["Name", "Emoji"]
        combo_list = []
        for emoji in self.client.get_all_emojis():
            combo_list.append([emoji.name, str(emoji)])
            if len(combo_list) == 30:
                full_message = tabulate.tabulate(combo_list, headers=head, tablefmt="simple")
                await self.client.send_message(p_message.author, full_message)
                del combo_list[:]
        if len(combo_list) != 0 or combo_list is not None:
            full_message = tabulate.tabulate(combo_list, headers=head, tablefmt="simple")
            await self.client.send_message(p_message.author, full_message)
