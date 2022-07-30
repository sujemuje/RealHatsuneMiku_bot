import discord
import voice_commands
from math import sqrt
import time
import os

TOKEN = os.environ['TOKEN']

ffmpeg_path = 'FFMPEG'

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client=client)


tree.add_command(voice_commands.__command_join)
tree.add_command(voice_commands.__command_play)
tree.add_command(voice_commands.__command_loop)


# DODAJ/ZABIERZ ROLE


@tree.command(
    name='dodaj_role',
    description='Dodaje role użytkownikowi'
)
async def __command_dodaj_role(
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role
) -> None:
    await member.add_roles(role)
    await interaction.response.send_message('dodano')


@tree.command(
    name='zabierz_role',
    description='Zabiera role użytkownikowi'
)
async def __command_zabierz_role(
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role
) -> None:
    await member.remove_roles(role)
    await interaction.response.send_message('zabrano')


# OBSŁUGA CZŁONKÓW SERWERA


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
    name='zmien_pseudonim',
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


# MINIGRA


@tree.command(
    name='typing_speedrun',
    description='Gra w jak najszybsze przepisanie wylosowanego ciągu znaków'
)
async def __command_typing_speedrun(
        interaction: discord.Interaction
) -> None:
    string = 'abcde'   # str = randomstring
    await interaction.response.send_message(f'Przepisz tekst: `{string}`!')

    def check(m):
        return m.channel == interaction.channel

    time_limit = 15.0

    TIME_S = time.time()
    msg = await client.wait_for('message', check=check, timeout=time_limit)
    TIME_E = time.time()

    while msg.content.lower() != string:
        time_delta = TIME_E - TIME_S
        time_limit -= time_delta

        TIME_S = time.time()
        msg = await client.wait_for('message', check=check, timeout=time_limit)
        TIME_E = time.time()

    time_delta = TIME_E - TIME_S
    time_limit -= time_delta
    await interaction.edit_original_message(content=f'Gratulacje, przepisałeś: `{string}` w {15.0 - time_limit} sekund!')


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


client.run(TOKEN)