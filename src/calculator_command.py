import discord
import calculator
# import custom_client


def init(tree):

    class CalculatorButton(discord.ui.Button):
        def __init__(self, value, calc, *args, **kwargs):
            self.value: int = value
            super().__init__(*args, **kwargs)
            self.calc = calc

        async def callback(self, interaction: discord.Interaction):
            # interaction.client.calculators[interaction.original_message().fetch().id]
            for child in self.view.children:
                if child.style == discord.ButtonStyle.green:
                    child.style = discord.ButtonStyle.gray
                    break
            self.style = discord.ButtonStyle.green

            self.calc.execute(self.label)
            await interaction.response.edit_message(content=self.calc.get_result(), view=self.view)

    class CalculatorView(discord.ui.View):
        """Reprezentacja kalkulatora za pomocą przycisków pod wiadomością, WIP"""

        def __init__(self, calc):
            super().__init__()
            self.calc = calc

            for y in range(4):
                for x in range(4):
                    if x < 3 and y < 3:
                        v = 6 - (3 * y) + x + 1
                        l = str(v)
                    else:
                        v = -1
                        l = ' '
                        if x == 1 and y == 3:
                            v = 0
                            l = '0'
                        elif x == 2 and y == 3:
                            l = '.'
                        elif x == 3:
                            if y == 0:    l = '+'
                            elif y == 1:  l = '-'
                            elif y == 2:  l = '*'
                            elif y == 3:  l = '/'
                        else:
                            v = -2
                            l = 'C'
                    self.add_item(CalculatorButton(
                        value=v,
                        calc=self.calc,
                        label=l,
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
        x: calculator.Calculator = calculator.Calculator()  # interaction)
        view = CalculatorView(x)
        await interaction.response.send_message(content='0', view=view)
        #client: custom_client.Client = interaction.client

        #client.calculators[interaction.original_message().fetch().id] = calculator.Calculator(interaction)
