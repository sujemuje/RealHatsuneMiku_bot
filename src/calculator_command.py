import discord


def init(tree):
    result: float = 0
    operation: str = ''
    recent: int = 0

    class CalculatorButton(discord.ui.Button):
        def __init__(self, value, *args, **kwargs):
            self.value: int = value
            super().__init__(*args, **kwargs)
            global recent

        async def callback(self, interaction: discord.Interaction):
            result = self.value
            # self.view.children[recent].style = discord.ButtonStyle.gray
            # recent = self.value"""cos sie przez to jebie, chyba klasy nie moga modyfikowac zmiennych z zewnatrz???"""
            """Inna metoda"""
            for child in self.view.children:
                if child.style == discord.ButtonStyle.green:
                    child.style = discord.ButtonStyle.gray
                    break
            """ """
            self.style = discord.ButtonStyle.green
            await interaction.response.edit_message(content=result, view = self.view)

    class CalculatorView(discord.ui.View):
        """Reprezentacja kalkulatora za pomocą przycisków pod wiadomością, WIP
        Na razie zrobiłem interakcję przycisków z 'wyświetlaczem'
        (treścią wiadomości bota na której wypisywany jest wynik)"""

        def __init__(self):
            super().__init__()
            for y in range(3):
                for x in range(3):
                    self.add_item(CalculatorButton(
                        value=(3 * y + x + 1),
                        label=str(3 * y + x + 1),
                        row=y,
                        style=discord.ButtonStyle.gray)
                    )

    @tree.command(
        name='kalkulator',
        description='prosty kalkulator guziczkowy'
    )
    async def __command_kalkulator(
            interaction: discord.Interaction
    ) -> None:
        view = CalculatorView()
        await interaction.response.send_message(content=result, view=view)
