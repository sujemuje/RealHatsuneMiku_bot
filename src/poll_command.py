import discord
from typing import *


class MyModal(discord.ui.Modal):
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
            content += f'\n{i} - {option.value}'
        await interaction.response.send_message(content=content, view=None)  # placeholder for button voting or sth


emotes = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':zero:']


class PollButton(discord.ui.Button):
    def __init__(self, order):
        self.order = order
        super().__init__(emoji=discord.PartialEmoji(name=':one:'))

    async def callback(self, interaction: discord.Interaction) -> None:
        for child in self.view.children:
            child.disabled = True
        await interaction.response.send_message(
            content=f'Użytkownik {interaction.user} zagłosował na opcję nr {self.order}!',
            view=self.view
        )


class PollView(discord.ui.View):
    def __init__(self, opt_count: int):
        super().__init__()
        for opt in range(opt_count):
            self.add_item(PollButton(order=opt))


def init(tree):
    @tree.command(
        name='poll',
        description='Creates a poll. Max 10 options'
    )
    async def __command_poll(
            interaction: discord.Interaction,
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

        view = PollView(opt_count=i)
        await interaction.response.send_message(content=content, view=view)

