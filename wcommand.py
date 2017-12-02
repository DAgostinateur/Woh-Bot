from util import *
from commands.Addadminuser import Addadminuser
from commands.Addchannelbd import Addchannelbd
from commands.Adduserbd import Adduserbd
from commands.City import City
from commands.Listadminuser import Listadminuser
from commands.Listalluserbd import Listalluserbd
from commands.Listemojis import Listemojis
from commands.Listuserbd import Listuserbd
from commands.Opentv import Opentv
from commands.React import React
from commands.Removeadminuser import Removeadminuser
from commands.Removechannelbd import Removechannelbd
from commands.Removeuserbd import Removeuserbd
from commands.Setpresence import Setpresence
from commands.Showchannelbd import Showchannelbd
from commands.Town import Town
from commands.Woh import Woh


def _command_list(p_client):
    cmd_list = [Addadminuser(p_client), Addchannelbd(p_client), Adduserbd(p_client), City(p_client),
                Listadminuser(p_client), Listalluserbd(p_client), Listemojis(p_client), Listuserbd(p_client),
                Opentv(p_client), React(p_client), Removeadminuser(p_client), Removechannelbd(p_client),
                Removeuserbd(p_client), Setpresence(p_client), Showchannelbd(p_client), Town(p_client), Woh(p_client)]

    return cmd_list


class WCommand:
    """Class that contains every command Woh Bot has."""

    def __init__(self, client):
        """Keyword arguments:
        client -- discord.Client()"""
        self.client = client
        self.commands = _command_list(client)

    async def command_checker(self, p_message):
        for command in self.commands:
            await command.command(p_message)

    def normal_message(self):
        normal_list = []
        message = NORMAL_MESSAGE_START.format(PREFIX)

        for command in self.commands:
            if command.permissionLevel == PERM_LEVEL_NORMAL:
                cmd_str = "{0}{1}".format(command.__str__(), command.cmdArguments)
                doc = command.get_doc()
                cmd_des = doc.format(command.cmdDoc)
                normal_list.append([cmd_str, cmd_des])

        message += tabulate.tabulate(normal_list, headers=["Command", "Description"], tablefmt="simple")
        final_msg = code_format(message, "")
        return final_msg

    def admin_message(self):
        admin_list = []
        message = ADMIN_MESSAGE_START

        for command in self.commands:
            if command.permissionLevel == PERM_LEVEL_ADMIN:
                cmd_str = "{0}{1}".format(command.__str__(), command.cmdArguments)
                doc = command.get_doc()
                cmd_des = doc.format(command.cmdDoc)
                admin_list.append([cmd_str, cmd_des])

        message += tabulate.tabulate(admin_list, headers=["Command", "Description"], tablefmt="simple")
        final_msg = code_format(message, "")
        return final_msg

    def owner_message(self):
        owner_list = []
        message = OWNER_MESSAGE_START

        for command in self.commands:
            if command.permissionLevel == PERM_LEVEL_OWNER:
                cmd_str = "{0}{1}".format(command.__str__(), command.cmdArguments)
                doc = command.get_doc()
                cmd_des = doc.format(command.cmdDoc)
                owner_list.append([cmd_str, cmd_des])

        message += tabulate.tabulate(owner_list, headers=["Command", "Description"], tablefmt="simple")
        final_msg = code_format(message, "")
        return final_msg
