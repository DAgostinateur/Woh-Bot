from util import *
from commands import WCommand

# TODO:
# - Remake every help messages. Right now it's hardcoded.
#           Make a list of command_name and command_description
#
# - Updates m_EmojiList, m_MemberList, m_ChannelList when one of them is added, removed or updated:
#           Will probably be in a different .py file.
#
# - Custom prefix for every server
# - A way for my friends to use emoji reactions from my Emoji Server
#           Example: r:Loss: -> The bot will see this as a call for reaction,
#                               it will react with said emoji on the previous message.
#                               It will also remove the call.
#                               When they react afterwards, the bot will remove his reaction.
#                               In the future you will be able to choose which message with id or index.
#
# - Open and close my Terraria and Gmod server:
#           Send the Terraria console output on the channel made for it and recieve input
#
# - Maybe some sort of game
# - Optimization
# - Make everything easier to read

client = discord.Client()

def HappyBirthdayMessage(p_mm_dd : str, p_serverId : str):
    BdMessage = ""
    HappyB = "{} Happy Birthday ".format(ObtainEmojiWithName(m_EmojiList, "woh"))
    userBdToday = []

    # Checking the date and checking the user's server, then adding him/her to userBdToday[]: 
    for userBd in m_UserBDList:
        if p_mm_dd == userBd.bd and p_serverId == ObtainMemberInfo(m_MemberList, userBd.userId, "si", p_serverId):
            userBdToday.append(userBd)

    if len(userBdToday) != 0: # Checks if there's anyone in userBdToday[]
        for nbUser in userBdToday:
            BdMessage = BdMessage + HappyB + UserFormat(nbUser.userId) + "\n\n"
        return BdMessage
    else:
        return ""


async def HappyBirthdayTimer():
    await client.wait_until_ready()
    while not client.is_closed:
        mm_dd = str(date.today())[5:]
        for server in m_ServerList:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == server.id:
                    text = HappyBirthdayMessage(mm_dd, server.id)
                    if text != "":
                        await client.send_message(discord.Object(id=channelBD.channelId), text)

        today_n = datetime.today()
        today_t = datetime.today()
        try:
            today_t = today_n.replace(day=today_n.day + 1, hour=11, minute=0, second=0, microsecond=0)
        except ValueError:
            try:
                # Only time it will go there is at the end of the month, except December:
                today_t = today_n.replace(month=today_n.month + 1, day=1, hour=11, minute=0, second=0, microsecond=0)
            except ValueError:
                # Only time it will go there is on December 30th:
                today_t = today_n.replace(year=today_n.year + 1, month=1, day=1, hour=11, minute=0, second=0, microsecond=0)

        delta_secs = int((today_t - today_n).seconds + 1)
        print(today_n)
        await asyncio.sleep(delta_secs) # Task runs every day at 11h00am

    
@client.event
async def on_ready():
    ExtractInfo(client)
    print(ConsoleMessage(client))
    # Doesn't work, no idea why:
    game = discord.Game(name="{0}{1} for help".format(PREFIX, WCommand.woh.__name__))
    await client.change_presence(game=game, status=discord.Status.online)


@client.event
async def on_reaction_add(reaction, user):
    if False: 
        reaction = discord.Reaction() # Only there to help me, this breaks the bot
        user = discord.User()         # Only there to help me, this breaks the bot

    if user == client.user:
        return

    if reaction.emoji == ObtainEmojiWithName(m_EmojiList, "woh"):
        await client.add_reaction(reaction.message, reaction.emoji)


@client.event
async def on_message(message):
    if False:
        message = discord.Message(message) # Only there to help me, this breaks the bot

    if message.author == client.user: # This prevents the bot from responding to itself
        return
    
    #WOH REACTION_START
    if "woh" in message.content.lower():
        await client.add_reaction(message, ObtainEmojiWithName(m_EmojiList, "woh"))
    #WOH REACTION_END

    wCommand = WCommand(client, message)
    await wCommand.woh(permissions="normal")
    await wCommand.openTV(permissions="owner")
    await wCommand.town(permissions="normal")
    await wCommand.city(permissions="normal")
    await wCommand.listAllUserBD(permissions="owner")
    await wCommand.listUserBD(permissions="normal")
    await wCommand.addUserBD(permissions="normal")
    await wCommand.removeUserBD(permissions="normal")
    await wCommand.showChannelBD(permissions="admin")
    await wCommand.addChannelBD(permissions="admin")
    await wCommand.removeChannelBD(permissions="admin")
    await wCommand.listAdminUser(permissions="owner")
    await wCommand.addAdminUser(permissions="owner")
    await wCommand.removeAdminUser(permissions="owner")


client.loop.create_task(HappyBirthdayTimer())
client.run(Token())
