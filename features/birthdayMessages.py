import asyncio
from datetime import date

from util import *


def happy_birthday_message(p_client, p_mm_dd: str, p_server_id: str):
    bd_message = ""
    happy_b = HAPPY_BIRTHDAY_START.format(obtain_emoji_with_name(p_client.get_all_emojis(), "woh"))
    user_bd_today = []

    # Checking the date and checking the user's server, then adding him/her to user_bd_today[]:
    for userBd in m_UserBDList:
        if p_mm_dd == userBd.bd and p_server_id == obtain_member_info(p_client.get_all_members(), userBd.userId, "si",
                                                                      p_server_id):
            user_bd_today.append(userBd)

    if len(user_bd_today) != 0:  # Checks if there's anyone in user_bd_today[]
        for nbUser in user_bd_today:
            bd_message = bd_message + happy_b + user_format(nbUser.userId) + "\n\n"
        return bd_message
    else:
        return ""


async def happy_birthday_timer(p_client):
    await p_client.wait_until_ready()
    while not p_client.is_closed:
        mm_dd = str(date.today())[5:]
        for server in m_ServerList:
            for channelBD in m_ChannelBDList:
                if channelBD.serverId == server.id:
                    text = happy_birthday_message(p_client, mm_dd, server.id)
                    if text != "":
                        await p_client.send_message(discord.Object(id=channelBD.channelId), text)

        print(datetime.today())  # Useful for console
        await asyncio.sleep(get_next_day_delta(11))  # Task runs every day at 11h00
