from util import *
from wcommand import WCommand
from features import birthdayMessages


# TODO:
# - Open and close my Terraria and Gmod server:
#           Send the Terraria console output on the channel made for it and receive input.
#           Learn about this, than I should be able to do it.
#
# - Remake Redbot's CustomCommands:
#           More options: !cmd -d  |> Deletes the message that calls the command.
#           Options will be entered as Linux parameters.
#
# - Reinstall discord.py:
#           Apparently, having multiple versions break some things, like change_presence.
#           This might be wrong.
#
# - Custom prefix for every server.
# - Optimization.
# - Log everything.
# - Music
# - Maybe some sort of game:
#           Incremental game for my bot where the entire server participates in passively or actively.

client = discord.Client()
wCommand = WCommand(client)


@client.event
async def on_ready():
    extract_info(client, wCommand)
    print(CONSOLE_MESSAGE.format(str(client.user)))


@client.event
async def on_member_join(member):
    if False:
        member = discord.Member()

    if member.server.id == my_server():
        human_count = obtain_server_count(member.server)
        client.edit_server(my_server(), name="{0}{1}".format(human_count, my_server_name()))


@client.event
async def on_member_remove(member):
    if False:
        member = discord.Member()

    if member.server.id == my_server():
        human_count = obtain_server_count(member.server)
        client.edit_server(my_server(), name="{0}{1}".format(human_count, my_server_name()))


@client.event
async def on_reaction_add(reaction, user):
    if False:
        reaction = discord.Reaction()
        user = discord.User()

    if user == client.user:
        return

    emoji = ""
    try:
        emoji = obtain_emoji_with_name(client.get_all_emojis(), "woh")
    except EmojiNameNonExistent:
        pass

    if reaction.emoji == emoji:
        await client.add_reaction(reaction.message, reaction.emoji)


@client.event
async def on_message(message):
    if False:
        message = discord.Message()  # Only there to help me, this breaks the bot

    if message.author == client.user:  # This prevents the bot from responding to itself
        return

    if "woh" in message.content.lower():
        try:
            await client.add_reaction(message, obtain_emoji_with_name(client.get_all_emojis(), "woh"))
        except EmojiNameNonExistent:
            # I'm not sending any messages to alert myself, it would be very spammy
            pass
    await wCommand.command_checker(message)


client.loop.create_task(birthdayMessages.happy_birthday_timer(client))
client.run(token())
