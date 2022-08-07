import discord


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


def init(tree):
    @tree.command(
        name='poll',
        description='Creates a poll. Max 5 options'
    )
    async def __command_poll(
            interaction: discord.Interaction,
            title: str,
            options: int
    ) -> None:
        modal = MyModal(title=title, options=options)
        await interaction.response.send_modal(modal)

