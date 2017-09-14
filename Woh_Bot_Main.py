import discord
from datetime import datetime
from datetime import date
import asyncio
import subprocess
import os
from tabulate import tabulate #https://pypi.python.org/pypi/tabulate
from util import *
from hidden import * #Things that I don't want to have seen by the public
                     #I'm the only one with access to this

#TODO LIST :
#- More user friendly removal of birthdays
#- Setting the BD channel with a command
#- Server checker, preventing the bot from sending a message to the wrong server
#- List of users that has access to BD commands

client = discord.Client()
m_EmojiList = []
m_MemberList = []
m_UserBDList = []
m_ChannelBDList = []
Prefix = '!' #The prefix that will be used for commands
HelpMessage = """**My prefix is [{0}].
Here's my list of commands:**
- {0}city [someone] -> Population of the city
- {0}town [someone] -> Population of the town
- {0}addBD [@user] [mm-dd] -> Adds a user to my birthday list
- {0}removeBD [@user] [mm-dd] -> Removes a user from my birthday list
- {0}listBD -> Lists everyone from my birthday list""".format(Prefix)


def HappyBirthdayMessage(p_mm_dd : str):
    BdMessage = ""
    HappyB = "Woh! Happy Birthday "
    userBdToday = []

    for userBd in m_UserBDList:
        if p_mm_dd == userBd.bd: #We're checking for people's birthdays and adding them to userBdToday[]
            userBdToday.append(userBd)

    if len(userBdToday) != 0: #We're checking if there's anyone in userBdToday[]
        for nbUser in userBdToday:
            BdMessage = BdMessage + HappyB + nbUser.userId + "\n\n"
        return BdMessage
    else:
        return ""


async def HappyBirthdayTimer():
    await client.wait_until_ready()
    while not client.is_closed:
        mm_dd = str(date.today())[5:]
        text = HappyBirthdayMessage(mm_dd)
        if text != "":
            await client.send_message(discord.Object(id='293438398050598912'), text) #The channelID is #discussion

        today_n = datetime.today()
        today_t = today_n.replace(day=today_n.day + 1, hour=11, minute=0, second=0, microsecond=0)
        delta_secs = int((today_t - today_n).seconds + 1)
        print(today_n)
        while True:
            try:
                await asyncio.sleep(delta_secs) # task runs every day at 11am
                break
            except Exception:
                print("Retry")


@client.event
async def on_ready():

    #COLLECTION_START
    for server in client.servers:
        for member in server.members: #Collects every Member from every server
            m_MemberList.append(member)
        for emoji in server.emojis: #Collects every Emoji from every server
            m_EmojiList.append(emoji)
    FileExtractBD(m_UserBDList)
    print("List of UserBD has been extracted.") #Collects every UserBd from FileNameUserBD()
    print("List of Emojis has been extracted.")
    print("List of Members has been extracted.")
    #COLLECTION_END
    print("---------\nWoh Bot\n---------")
    print("Logged in as " + str(client.user))
    print("Creator : D'Agostinateur Woh")
    print("---------")


@client.event
async def on_reaction_add(reaction, user):
    if user != client.user: #Idk if it would cause an infinite loop without this
        if reaction.emoji == ObtainEmojiWithName(m_EmojiList, "woh"):
             await client.add_reaction(reaction.message, ObtainEmojiWithName(m_EmojiList, "woh"))


@client.event
async def on_message(message):
    if message.author != client.user: #This prevents the bot from responding to itself

        #HELP_START
        if message.content.startswith(Prefix + "help"):
            await client.send_message(message.author, HelpMessage)
            await client.delete_message(message)
            if message.author.id == MyID():
                extraHelp = "**You are allowed see and use these special commands.**\n- {0}openTV -> Opens TeamViewer\n- {0}closeTV -> Closes TeamViewer ".format(Prefix)
                await client.send_message(message.author, extraHelp)
        #HELP_END

        #WOH REACTION_START
        if "woh" in message.content.lower():
            await client.add_reaction(message, ObtainEmojiWithName(m_EmojiList, "woh")) # DISCORD EXPLOIT, THE BOT CAN SEND THIS EVEN IF THE SERVER DOESN'T HAVE THE EMOJI
        #if "woh" in message.content.lower():
        #    await client.send_message(message.channel, ObtainEmojiWithName(EmojiList, "woh"))
        #WOH REACTION_END

        #OPEN TEAMVIEWER_START
        if message.content.startswith(Prefix + "openTV"):
            if message.author.id == MyID:
                await client.send_message(message.channel, "Opening TeamViewer...")
                subprocess.call(CmdOpenTV()) #Opens TeamViewer.exe
            else:
                await client.send_message(message.channel, "**You do not have access to this command**")
        #OPEN TEAMVIEWER_END
        #CLOSE TEAMVIEWER_START
        if message.content.startswith(Prefix + "closeTV"):
            if message.author.id == MyID():
                await client.send_message(message.channel, "Closing TeamViewer...")
                os.system(CmdCloseTV()) #Closes TeamViewer.exe
            else:
                await client.send_message(message.channel, "**You do not have access to this command**")
        #CLOSE TEAMVIEWER_END

        #TOWN_START
        if message.content.startswith(Prefix + "town"):
            command = str(message.content)[6:] #Removes the "!town " from the content
            if len(command) != 0:
                msg = "Shut the Fuck Up Town\nPopulation: {}".format(command)
                await client.send_message(message.channel, msg)
                await client.delete_message(message)
        #TOWN_END
        #CITY_START
        if message.content.startswith(Prefix + "city"):
            command = str(message.content)[6:] #Removes the "!city " from the content
            if len(command) != 0:
                msg = "Gotem City\nPopulation: {}".format(command)
                await client.send_message(message.channel, msg)
                await client.delete_message(message)
        #CITY_END

        #LIST BIRTH DATES_START
        if message.content.startswith(Prefix + "listBD"):
            if len(m_UserBDList) != 0:
                comboList = []
                for userBd in m_UserBDList:
                    name = ObtainMemberInfo(m_MemberList, userBd.ObtainPureUserID(), "na")
                    comboList.append([name, userBd.bd])
                    if len(comboList) == 10:
                        fullMessage = "```" + tabulate(comboList, headers=["Name", "Birthday"], tablefmt="fancy_grid") + "```"
                        await client.send_message(message.author, fullMessage)
                        del comboList
                if len(comboList) != 0 or comboList is not None:
                    fullMessage = "```" + tabulate(comboList, headers=["Name", "Birthday(mm-dd)"], tablefmt="fancy_grid") + "```"
                    await client.send_message(message.author, fullMessage)
            else:
                await client.send_message(message.author, "The list is empty.")
        #LIST BIRTH DATES_END
        #BIRTHDAY ADDER_START
        if message.content.startswith(Prefix + "addBD"):
            #await client.send_message(message.channel, "Command deactivated.")
            #return #COMMMAND DEACTIVATED
            command = str(message.content)[7:] #Removes the "!addBD " from the content
            userId = ""
            bd = ""
            if len(command.split()) == 2: #Needs the user id and date, so 2 parameters
                for parameter in command.split():
                    if "@" in parameter: #The UserId
                        userId = str(parameter)
                    elif "-" in parameter: #The BirthDate
                        bd = str(parameter)
                    else:
                        await client.send_message(message.channel, "**[@user](or <@!id>) or [mm-dd]** was not entered correctly.")
                        return
                try:
                    bdTest = datetime.strptime(bd, "%m-%d") #Verifying the date
                except ValueError:
                    await client.send_message(message.channel, "**Invalid date**, make sure you entered possible dates.")
                    return

                if not IsUserIdValid(m_MemberList, userId):
                    await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from the server.")
                    return

                await client.send_message(message.channel, "Added birthday.") #If this sends a message, it means everything is valid
            else:
                await client.send_message(message.channel, "Use the command this way : !addBD [@user](or <@!id>) [mm-dd]")
                return

            FileAddBD(m_UserBDList, userId, bd)
        #BIRTHDAY ADDER_END
        #BIRTHDAY REMOVER_START
        if message.content.startswith(Prefix + "removeBD"):
            #await client.send_message(message.channel, "Command deactivated.")
            #return #COMMMAND DEACTIVATED
            command = str(message.content)[10:] #Removes the "!removeBD " from the content
            userId = ""
            bd = ""
            if len(m_UserBDList) == 0:
                await client.send_message(message.channel, "There's nobody to remove from my birthday list.")
                return

            if len(command.split()) == 2: #Needs the user id and date, so 2 parameters
                for parameter in command.split():
                    if "@" in parameter: #The UserId
                        userId = str(parameter)
                    elif "-" in parameter: #The BirthDate
                        bd = str(parameter)
                    else:
                        await client.send_message(message.channel, "**[@user](or <@!id>) or [mm-dd]** was not entered correctly.")
                        return
                try:
                    bdTest = datetime.strptime(bd, "%m-%d") #Verifying the date
                except ValueError:
                    await client.send_message(message.channel, "**Invalid date**, make sure you entered possible dates.")
                    return

                if not IsUserIdValid(m_MemberList, userId):
                    await client.send_message(message.channel, "**Invalid user**, make sure you entered a real user from the server.")
                    return

            listIndex = 0 #We're sending the index to FileRemoveBD
            for userBd in m_UserBDList: #If the code reaches this, it means everything is valid
                if userId == userBd.userId and userBd.bd == bd:
                    FileRemoveBD(m_UserBDList, listIndex)
                    await client.send_message(message.channel, "Removed birthday.") 
                    return
                listIndex += 1
            await client.send_message(message.channel, "**User with this date is not in my list.**") 
        #BIRTHDAY REMOVER_END


client.loop.create_task(HappyBirthdayTimer())
client.run(Token())
