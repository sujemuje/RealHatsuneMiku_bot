import discord
import calculator
# import custom_client


def init(tree):

    class CalculatorButton(discord.ui.Button):
        """
        Reprezentacja przycisku kalkulatora za pomocą discord.ui.Button
        """
        def __init__(self, calc, *args, **kwargs):
            """
            Inicjalizacja klasy
            :param calc: obiekt klasy Calculator; odpowiada za obliczeniową stronę całej komendy
            """
            super().__init__(*args, **kwargs)
            self.calc = calc

        async def callback(self, interaction: discord.Interaction) -> None:
            """
            Reakcja na naciśnięcie przycisku
            :param interaction: discord.Interaction
            :return: None
            """
            # Aktualizacja koloru przycisków
            for child in self.view.children:
                if child.style == discord.ButtonStyle.green:
                    child.style = discord.ButtonStyle.gray
                    break
            self.style = discord.ButtonStyle.green

            # Przekazanie danych o naciśniętym przycisku; odpowiednimi reakcjami zarządza metoda klasy Calculator
            self.calc.execute(self.label)
            # Aktualizacja komendy
            await interaction.response.edit_message(content=self.calc.get_result(), view=self.view)

    class CalculatorView(discord.ui.View):
        """
        Reprezentacja kalkulatora za pomocą discord.ui.View zawierającego przyciski - CalculatorButton
        """
        def __init__(self, calc):
            """
            Inicjalizacja klasy
            :param calc: obiekt klasy Calculator;
            będzie przekazywany przyciskom, by te mogły wywoływać na nim odpowiednią metodę przy callbacku
            """
            super().__init__()
            self.calc = calc

            # Tworzenie przycisków z odpowiednimi podpisami
            for y in range(4):
                for x in range(4):
                    if x < 3 and y < 3:
                        label = str(6 - (3 * y) + x + 1)
                    else:
                        label = ' '
                        if x == 1 and y == 3:
                            label = '0'
                        elif x == 2 and y == 3:
                            label = '.'
                        elif x == 3:
                            if y == 0:
                                label = '+'
                            elif y == 1:
                                label = '-'
                            elif y == 2:
                                label = '*'
                            elif y == 3:
                                label = '/'
                        else:
                            label = 'C'
                    self.add_item(CalculatorButton(
                        calc=self.calc,
                        label=label,
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
        calc: calculator.Calculator = calculator.Calculator()
        view = CalculatorView(calc)
        await interaction.response.send_message(content='0', view=view)
