# GENERAL IMPORTS
import os
import discord
import aiohttp
import custom_client
# COMMAND IMPORTS
import poll_command
import voice_commands
import typing_speedrun
import calculator_command
import add_and_reset
import image_command
# COMMAND TREE IMPORTS
import role_tree


# CLIENT AND COMMAND TREE


intents = discord.Intents.all()
client = custom_client.Client(intents=intents)
tree = discord.app_commands.CommandTree(client=client)
tree.add_command(role_tree.group_role)


# INITS

poll_command.init(tree)
typing_speedrun.init(tree)
voice_commands.init(tree)
calculator_command.init(tree)
add_and_reset.init(tree)
image_command.init(tree)

# TESTS


# GUILD MEMBERS MANAGEMENT


@tree.command(
    name='wypisz_aktywnych',
    description='Wypisuje wszystkich użytkowników Discorda ze statusem "Aktywny"'
)
async def __command_wypisz_aktywnych(
        interaction: discord.Interaction
) -> None:
    online_members = []
    for member in interaction.guild.members:
        if member.status == discord.Status.online:
            online_members.append(member.name)
    await interaction.response.send_message('\n'.join(online_members))


@tree.command(
    name='pseudonim',
    description='Zmienia pseudonim wybranego użytkownika'
)
async def __command_zmien_pseudonim(
        interaction: discord.Interaction,
        member: discord.Member,
        new_nick: str
) -> None:
    await member.edit(nick=new_nick)
    await interaction.response.send_message(
        f'Pomyślnie zmieniono pseudonim użytkownika {member.name} na {new_nick}'
    )


@tree.command(
    name='dm_sb',
    description='Pisze podaną wiadomość do wybranego użytkownika'
)
async def __command_dm_me(
        interaction: discord.Interaction,
        member: discord.Member,
        msg: str
) -> None:
    await interaction.response.send_message('Wiadomość dostarczona pomyślnie', ephemeral=True)
    await member.send(msg)


# ON READY


@client.event
async def on_ready():
    game = discord.Game("with deez nuts")
    await client.change_presence(status=discord.Status.idle, activity=game)
    print('ready')
    await tree.sync()


# SIMPLE ON_TYPE/MESSAGE/REACTION EVENTS


@client.event
async def on_message(message: discord.Message):
    if message.content == "123":
        await message.channel.send("456")


@client.event
async def on_typing(channel: discord.TextChannel, user, when):
    if user != client.user:
        await channel.typing()


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.add_reaction(payload.emoji)


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, client.user)


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
