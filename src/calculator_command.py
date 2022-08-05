import discord


result: float = 0
text_buffer: [str] = ['0', '']
operation: chr = '+'
recent: int = -1


def init(tree):
    def compute(oper: chr):
        global text_buffer, operation, result
        if operation == '+':
            result = int(text_buffer[0]) + int(text_buffer[1])
        elif operation == '-':
            result = int(text_buffer[0]) - int(text_buffer[1])
        elif operation == '*':
            result = int(text_buffer[0]) * int(text_buffer[1])
        elif operation == '/':
            result = int(text_buffer[0]) / int(text_buffer[1])
        text_buffer[0] = str(result)
        text_buffer[1] = ''
        operation = oper

    class CalculatorButton(discord.ui.Button):
        def __init__(self, value, *args, **kwargs):
            self.value: int = value
            global recent
            self.index = recent + 1
            recent += 1
            super().__init__(*args, **kwargs)

        async def callback(self, interaction: discord.Interaction):
            global recent
            self.view.children[recent].style = discord.ButtonStyle.gray
            recent = self.index
            """Inna metoda
            for child in self.view.children:
                if child.style == discord.ButtonStyle.green:
                    child.style = discord.ButtonStyle.gray
                    break
            """
            self.style = discord.ButtonStyle.green

            global text_buffer, result
            if self.value == -1:
                compute(self.label)
            else:
                text_buffer[1] += self.label
                result = text_buffer[1]
            await interaction.response.edit_message(content=result, view=self.view)

    class CalculatorView(discord.ui.View):
        """Reprezentacja kalkulatora za pomocą przycisków pod wiadomością, WIP
        Na razie zrobiłem interakcję przycisków z 'wyświetlaczem'
        (treścią wiadomości bota na której wypisywany jest wynik)"""

        def __init__(self):
            super().__init__()
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
                    self.add_item(CalculatorButton(
                        value=v,
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
        view = CalculatorView()
        await interaction.response.send_message(content=result, view=view)
