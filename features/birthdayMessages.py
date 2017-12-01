from util import *

def HappyBirthdayMessage(p_client, p_mm_dd : str, p_serverId : str):
    BdMessage = ""
    HappyB = HAPPY_BIRTHDAY_START.format(ObtainEmojiWithName(p_client.get_all_emojis(), "woh"))
    userBdToday = []

    # Checking the date and checking the user's server, then adding him/her to userBdToday[]: 
    for userBd in m_UserBDList:
        if p_mm_dd == userBd.bd and p_serverId == ObtainMemberInfo(p_client.get_all_members(), userBd.userId, "si", p_serverId):
            userBdToday.append(userBd)

    if len(userBdToday) != 0: # Checks if there's anyone in userBdToday[]
        for nbUser in userBdToday:
            BdMessage = BdMessage + HappyB + UserFormat(nbUser.userId) + "\n\n"
        return BdMessage
    else:
        return ""


async def HappyBirthdayTimer(p_client):
    await p_client.wait_until_ready()
    while not p_client.is_closed:
        mm_dd = str(date.today())[5:]
        for server in m_ServerList:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == server.id:
                    text = HappyBirthdayMessage(p_client, mm_dd, server.id)
                    if text != "":
                        await p_client.send_message(discord.Object(id=channelBD.channelId), text)

        print(datetime.today()) # Userful for the console
        await asyncio.sleep(GetNextDayDelta(11)) # Task runs every day at 11h00