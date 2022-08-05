import discord


def init(tree):
    result: float = 0.0
    operation: str = ''

    class CalculatorButton(discord.ui.Button):
        def __init__(self, value, *args, **kwargs):
            self.value = value
            super().__init__(label=str(value), *args, **kwargs)

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.edit_message(content=self.value)

    class CalculatorView(discord.ui.View):
        """Reprezentacja kalkulatora za pomocą przycisków pod wiadomością, WIP
        Na razie zrobiłem interakcję przycisków z 'wyświetlaczem'
        (treścią wiadomości bota na której wypisywany jest wynik)"""

        def __init__(self):
            super().__init__()
            global result
            global operation
            for y in range(3):
                for x in range(3):
                    self.add_item(CalculatorButton(value=(3 * y + x + 1), row=y))

    @tree.command(
        name='kalkulator',
        description='prosty kalkulator guziczkowy'
    )
    async def __command_kalkulator(
            interaction: discord.Interaction
    ) -> None:
        view = CalculatorView()
        await interaction.response.send_message(content='0', view=view)
