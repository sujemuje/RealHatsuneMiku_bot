import discord
from math import sqrt
import time
import os

TOKEN = os.environ['TOKEN']

ffmpeg_path = 'C:/Users/mateu/Desktop/Homework/ffmpeg-n5.1-latest-win64-gpl-5.1/bin'

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client=client)


@tree.command(
    name='miejsca_zerowe',
    description='Oblicza miejsca zerowe trójmianu kwadratowego i je wypisuje jeśli istnieją w R'
)
async def __command_miejsca_zerowe(
        interaction: discord.Interaction,
        a: float, b: float, c: float
) -> None:
    delta = b**2 - 4*a*c
    if delta < 0:
        await interaction.response.send_message("Brak miejsc zerowych w R")
    elif delta == 0:
        await interaction.response.send_message(f'{b / (2*a)}')
    else:
        await interaction.response.send_message(
            f'{(b + sqrt(delta)) / (2*a)}, {(b - sqrt(delta)) / (2*a)}'
        )


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
    await interaction.user.send("egg")
    await member.send(msg)


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


@tree.command(
    name='vc_connect',
    description='Łączy się z kanałem głosowym'
)
async def __command_vc_connect(
        interaction: discord.Interaction
) -> None:
    connected = False
    for vc_channel in interaction.guild.voice_channels:
        for member in vc_channel.members:
            if member == interaction.user:
                connected = True
                await vc_channel.connect()  # tu sie chyba tworzy voiceclient
                await interaction.response.send_message(
                    f'Połączono z kanałem {vc_channel.mention} na prośbę użytkownika {member.mention}')
                break
        if connected: break
    else:
        await interaction.response.send_message(f'Nie udało się połączyć z kanałem głosowym')


@tree.command(
    name='play',
    description='Odtwarza hymn Hatsune Miku'
)
async def __command_play(
        interaction: discord.Interaction
) -> None:
    if isinstance(interaction.user, discord.User):
        await interaction.response.send_message('Do użycia tylko na serwerach')
        return
    if interaction.user.voice is None:
        await interaction.response.send_message('Nie jesteś połączony z kanałem głosowym')
        return
    if interaction.guild.voice_client is None:
        await interaction.user.voice.channel.connect()
    else:
        await interaction.guild.voice_client.move_to(interaction.user.voice.channel)

    await interaction.response.send_message(
        f'Połączono z kanałem {interaction.user.voice.channel.mention} na prośbę użytkownika {interaction.user.mention}'
    )

    source = discord.FFmpegOpusAudio(source='./audio/HM.opus')
    interaction.guild.voice_client.play(source)


@client.event
async def on_ready():
    game = discord.Game("with deez nuts")
    await client.change_presence(status=discord.Status.idle, activity=game)
    print('ready')
    await tree.sync()


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