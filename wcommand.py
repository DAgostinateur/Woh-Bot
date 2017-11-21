from util import *
from commands.addAdminUser import addAdminUser
from commands.addChannelBD import addChannelBD
from commands.addUserBD import addUserBD
from commands.city import city
from commands.listAdminUser import listAdminUser
from commands.listAllUserBD import listAllUserBD
from commands.listUserBD import listUserBD
from commands.openTV import openTV
from commands.removeAdminUser import removeAdminUser
from commands.removeChannelBD import removeChannelBD
from commands.removeUserBD import removeUserBD
from commands.setPresence import setPresence
from commands.showChannelBD import showChannelBD
from commands.town import town
from commands.woh import woh


def _commandList(p_client):
   cmdList = []

   cmdList.append(addAdminUser(p_client))
   cmdList.append(addChannelBD(p_client))
   cmdList.append(addUserBD(p_client))
   cmdList.append(city(p_client))
   cmdList.append(listAdminUser(p_client))
   cmdList.append(listAllUserBD(p_client))
   cmdList.append(listUserBD(p_client))
   cmdList.append(openTV(p_client))
   cmdList.append(removeAdminUser(p_client))
   cmdList.append(removeChannelBD(p_client))
   cmdList.append(removeUserBD(p_client))
   cmdList.append(setPresence(p_client))
   cmdList.append(showChannelBD(p_client))
   cmdList.append(town(p_client))
   cmdList.append(woh(p_client))
   
   return cmdList

class WCommand():
    """Class that contains every command Woh Bot has."""
    def __init__(self, client):
        """Keyword arguments:
        client -- discord.Client()"""
        self.client = client
        self.commands = _commandList(client)


    async def commandChecker(self, p_message):
        for command in self.commands:
            await command.command(p_message)


    def normalMessage(self):
        normalList = []
        message = "My prefix is [{0}].\n".format(PREFIX)

        for command in self.commands:
            if command.permissionLevel == PERM_LEVEL_NORMAL:
                cmdStr = "{0}{1}".format(command.__str__(), command.cmdArguments)
                doc = command.getDoc()
                cmdDes = doc.format(command.cmdDoc)
                normalList.append([cmdStr, cmdDes])

        message += tabulate(normalList, headers=["Command", "Description"], tablefmt="fancy_grid")
        finalMsg = CodeFormat(message, "")
        return finalMsg
    

    def adminMessage(self):
        adminList = []
        message = "Admin commands.\n"

        for command in self.commands:
            if command.permissionLevel == PERM_LEVEL_ADMIN:
                cmdStr = "{0}{1}".format(command.__str__(), command.cmdArguments)
                doc = command.getDoc()
                cmdDes = doc.format(command.cmdDoc)
                adminList.append([cmdStr, cmdDes])

        message += tabulate(adminList, headers=["Command", "Description"], tablefmt="fancy_grid")
        finalMsg = CodeFormat(message, "")
        return finalMsg


    def ownerMessage(self):
        ownerList = []
        message = "Owner commands.\n"

        for command in self.commands:
            if command.permissionLevel == PERM_LEVEL_OWNER:
                cmdStr = "{0}{1}".format(command.__str__(), command.cmdArguments)
                doc = command.getDoc()
                cmdDes = doc.format(command.cmdDoc)
                ownerList.append([cmdStr, cmdDes])

        message += tabulate(ownerList, headers=["Command", "Description"], tablefmt="fancy_grid")
        finalMsg = CodeFormat(message, "")
        return finalMsg
