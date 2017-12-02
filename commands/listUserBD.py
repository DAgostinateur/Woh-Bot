from util import *
from cmdtemplate import Command


class Listuserbd(Command):
    """Lists everyone from my birthday list."""

    isDisabled = False
    permissionLevel = PERM_LEVEL_NORMAL

    def get_doc(self):
        return str(self.__class__.__doc__)

    def __str__(self):
        return str(self.__class__.__name__)

    def more_help(self):
        return MORE_HELP_LIST_USER_BD.format(self.__str__())

    async def command(self, p_message):
        """Actual Command"""
        if await self.execute_command(self.isDisabled, p_message, self.__str__(),
                                      self.permissionLevel, self.more_help()):
            return

        server_id = str(p_message.server.id)
        if len(m_UserBDList) != 0:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == server_id:
                    combo_list = []
                    for userBd in m_UserBDList:
                        if server_id == obtain_member_info(self.client.get_all_members(), userBd.userId, "si",
                                                           server_id):
                            name = obtain_member_info(self.client.get_all_members(), userBd.userId, "na", "")
                            combo_list.append([name, userBd.bd])
                        if len(combo_list) == 10:
                            full_message = code_format(
                                tabulate.tabulate(combo_list, headers=["Name", "Birthday(mm-dd)"],
                                                  tablefmt="fancy_grid"), "")
                            await self.client.send_message(p_message.author, full_message)
                            del combo_list[:]
                    if len(combo_list) != 0 or combo_list is not None:
                        full_message = code_format(
                            tabulate.tabulate(combo_list, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid"),
                            "")
                        await self.client.send_message(p_message.author, full_message)
        else:
            await self.client.send_message(p_message.author, EMPTY_LIST)
