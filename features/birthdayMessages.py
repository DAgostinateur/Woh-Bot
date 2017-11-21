from util import *

def HappyBirthdayMessage(p_client, p_mm_dd : str, p_serverId : str):
    BdMessage = ""
    HappyB = "{0} Happy Birthday ".format(ObtainEmojiWithName(p_client.get_all_emojis(), "woh"))
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
        print(today_n) # Userful for the console
        await asyncio.sleep(delta_secs) # Task runs every day at 11h00am