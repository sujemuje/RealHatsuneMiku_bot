import discord
from typing import *


"""class MyModal(discord.ui.Modal):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if options < 2: options = 2
        elif options > 5: options = 5
        for i in range(options):
            self.add_item(discord.ui.TextInput(label=f'option {i+1}'))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        content = f'{self.title}:'
        i = 0
        for option in self.children:
            i += 1
            content += f'{i} - {option.value}'
        await interaction.response.send_message(content=content, view=None)  # placeholder for button voting or sth
"""

emotes = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '0️⃣']


class OptionButton(discord.ui.Button):
    def __init__(self, order, public):
        self.order = order
        self.votes = 0
        self.public = public
        l = '0' if self.public else ' ❔'
        super().__init__(label=l, emoji=emotes[self.order])

    async def callback(self, interaction: discord.Interaction) -> None:
        for child in self.view.children:
            child.disabled = True
        self.votes += 1
        if self.public:
            self.view.children[-1].disabled = False
            self.view.children[-1].voters[self.order].append(interaction.user.mention)
            self.label = self.votes
        await interaction.response.edit_message(view=self.view)


class VotersButton(discord.ui.Button):
    def __init__(self, opt_count):
        super().__init__(label='List of voters', emoji='📜', style=discord.ButtonStyle.primary)
        self.voters: List[List] = [[] for i in range(opt_count)]

    async def callback(self, interaction: discord.Interaction):
        content = 'Lista użytkowników którzy zagłosowali:'

        for i in range(len(self.voters)):
            if self.voters[i]:
                content += f'\n{emotes[i]} : '
                for voter in self.voters[i]:
                    content += f'\n - {voter}'
                content += '\n'

        await interaction.response.send_message(content=content, ephemeral=True)


class PollView(discord.ui.View):
    def __init__(self, opt_count: int, public: bool):
        super().__init__()

        for opt in range(opt_count):
            self.add_item(OptionButton(order=opt, public=public))
        if public:
            self.add_item(VotersButton(opt_count=opt_count))

def init(tree):
    @tree.command(
        name='poll',
        description='Creates a poll. Max 10 options'
    )
    async def __command_poll(
            interaction: discord.Interaction,
            public: bool,
            title: str,
            opt1: str,
            opt2: str,
            opt3: Optional[str],
            opt4: Optional[str],
            opt5: Optional[str],
            opt6: Optional[str],
            opt7: Optional[str],
            opt8: Optional[str],
            opt9: Optional[str],
            opt10: Optional[str]
    ) -> None:
        # modal = MyModal(title=title, options=options)
        # await interaction.response.send_modal(modal)

        options = [opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10]
        content = f'{title}:'
        i = 0
        for option in options:
            if option is not None:
                content += f'\n{emotes[i]} - {option}'
                i += 1

        view = PollView(opt_count=i, public=public)
        await interaction.response.send_message(content=content, view=view)

