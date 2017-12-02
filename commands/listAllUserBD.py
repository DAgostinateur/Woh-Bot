from util import *
from cmdtemplate import Command


class Listalluserbd(Command):
    """Lists the entire birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_ADMIN

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_LIST_ALL_USER_BD.format(self.__str__())

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        if len(m_UserBDList) != 0:
            head = ["Name", "Birthday(mm-dd)", "User ID"]
            combo_list = []
            for userBd in m_UserBDList:
                member = obtain_member_info(self.client.get_all_members(), userBd.userId, "mb", "")
                combo_list.append([member.name, userBd.bd, member.id])
                if len(combo_list) == 10:
                    full_message = code_format(tabulate.tabulate(combo_list, headers=head, tablefmt="fancy_grid"), "")
                    await self.client.send_message(p_message.author, full_message)
                    del combo_list[:]
            if len(combo_list) != 0 or combo_list is not None:
                full_message = code_format(tabulate.tabulate(combo_list, headers=head, tablefmt="fancy_grid"), "")
                await self.client.send_message(p_message.author, full_message)
        else:
            await self.client.send_message(p_message.author, EMPTY_LIST)
