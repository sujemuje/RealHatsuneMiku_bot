class Calculator:
    def __init__(self):  # , interaction):
        self.result: str = '0'
        self.text_buffer: [str] = ['0', '']
        self.operator: chr = '+'
        # self.interaction_id = interaction.id

    def reset(self):
        self.result = '0'
        self.text_buffer = ['0', '']
        self.operator = '+'

    def execute(self, oper: chr):
        if oper == 'C':
            self.reset()
        elif oper == '+' or oper == '-' or oper == '*' or oper == '/':
            if self.text_buffer[1] != '':
                self.calculate()
            self.operator = oper
            self.result += f' {self.operator} '
        else:
            if oper == '.':
                if self.text_buffer[1] == '':
                    self.text_buffer[1] = '0'
                oper = '' if '.' in self.text_buffer[1] else oper
            self.text_buffer[1] += oper
            if self.result == '0':
                self.result = ''
            self.result += oper

    def calculate(self) -> None:
        self.result = str(eval(f'{self.text_buffer[0]}{self.operator}{self.text_buffer[1]}'))
        self.text_buffer[0] = self.result
        self.text_buffer[1] = ''

    def get_result(self):
        return self.result

    """def __hash__(self):
        return hash(self.interaction_id)"""
