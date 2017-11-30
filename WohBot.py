from util import *
from wcommand import WCommand
from features.birthdayMessages import HappyBirthdayTimer, HappyBirthdayMessage

# TODO:
# - User AdminUser().
# - Log everything.
#
# - Open and close my Terraria and Gmod server:
#           Send the Terraria console output on the channel made for it and recieve input.
#           Learn about this, than I should be able to do it.
#
# - Remake Redbot's CustomCommands:
#           More options: !cmd -d  |> Deletes the message that calls the command.
#           Options will be entered as Linux parameters.
#
# - !react command:
#           When the user react, the bot's reaction will be removed.
#
# - Reinstall discord.py:
#           Apparently, having multiple versions break some things, like change_presence.
#           This might be wrong.
#
# - Custom prefix for every server.
# - Optimization.
# - Music
# - Make everything easier to read/PEP8.
# - Maybe some sort of game:
#           Incremental game for my bot where the entire server participates in passively or actively.

client = discord.Client()
wCommand = WCommand(client)
    
@client.event
async def on_ready():
    ExtractInfo(client, wCommand)
    print(CONSOLE_MESSAGE.format(str(client.user)))


@client.event
async def on_member_join(member):
    if False:
        member = discord.Member()

    if member.server.id == MyServer():
        humanCount = ObtainServerCount(client.get_server(member.server.id), MyServer())
        client.edit_server(MyServer(), name="{0}{1}".format(humanCount, MyServerName()))


@client.event
async def on_member_remove(member):
    if False:
        member = discord.Member()

    if member.server.id == MyServer():
        humanCount = ObtainServerCount(client.get_server(member.server.id), MyServer())
        client.edit_server(MyServer(), name="{0}{1}".format(humanCount, MyServerName()))

@client.event
async def on_reaction_add(reaction, user):
    if False: 
        reaction = discord.Reaction()
        user = discord.User()

    if user == client.user:
        return

    if reaction.emoji == ObtainEmojiWithName(client.get_all_emojis(), "woh"):
        await client.add_reaction(reaction.message, reaction.emoji)


@client.event
async def on_message(message):
    if False:
        message = discord.Message(message) # Only there to help me, this breaks the bot

    if message.author == client.user: # This prevents the bot from responding to itself
        return
    
    #WOH REACTION_START
    if "woh" in message.content.lower():
        await client.add_reaction(message, ObtainEmojiWithName(client.get_all_emojis(), "woh"))
    #WOH REACTION_END

    await wCommand.commandChecker(message)


client.loop.create_task(HappyBirthdayTimer(client))
client.run(Token())
