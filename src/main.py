import discord
import voice_commands
import typing_speedrun
import os


TOKEN = os.environ['TOKEN']


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client=client)


typing_speedrun.init(tree, client)
voice_commands.init(tree)


# VIEW COMMANDS


class MyView(discord.ui.View):

    @discord.ui.button(
        label='k',
        style=discord.ButtonStyle.green,
        emoji='<a:pajmo:960818030735134730>'
    )
    async def button_callback(self, interaction, button):
        print(button)
        button.label = 'lol'
        await interaction.response.edit_message(content='kliknięto!', view=self)


@tree.command(
    name='test',
    description='test UI'
)
async def __command_test(
        interaction: discord.Interaction
) -> None:
    view = MyView()
    await interaction.response.send_message(content='kliknij przycisk...', view=view)


class CalculatorButton(discord.ui.Button):
    def __init__(self, val, *args, **kwargs):
        self.val = val
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        print(f'Wywołano przycisk o nazwie {self.label} i wartości {self.val}!')
        if self.val != 0:
            self.view.set_operation(self.label)
        else:
            if self.view.get_operation() == '+':
                self.view.set_result(self.view.get_result() + self.val)
            if self.view.get_operation() == '-':
                self.view.set_result(self.view.get_result() - self.val)
            else:
                self.view.set_result(self.val)
            print(self.view.get_result())
        await interaction.response.edit_message(content=self.view.get_result(), view=self.view)


class CalculatorView(discord.ui.View):
    """Reprezentacja kalkulatora za pomocą przycisków pod wiadomością.
    Na razie pracuje na intach z zakresu 0-9"""
    def __init__(self):
        super().__init__()
        self.result: int = 0
        self.operation: str = ''

        for y in range(3):
            for x in range(4):
                label: str
                val: int

                if x < 3:
                    val = 1 + x + 3 * y
                    label = str(val)
                else:
                    val = 0
                    if y == 0: label = '+'
                    elif y == 1: label = '-'
                    else: label = 'chuj'

                self.add_item(CalculatorButton(label=label, row=y, val=val))

    def on_callback(self):


    """async def button_callback(button, interaction: discord.Interaction):
        if val != 0:
            self.operation = button.label
        else:
            if self.operation == '+':
                self.result += int(button.label)
            if self.operation == '-':
                self.result -= int(button.label)
            else:
                self.result = int(button.label)
        interaction.response.edit_message(content=self.result)"""


@tree.command(
    name='kalkulator',
    description='prosty kalkulator guziczkowy'
)
async def __command_kalkulator(
        interaction: discord.Interaction
) -> None:
    view = CalculatorView()
    await interaction.response.send_message(content='0', view=view)


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