import discord
import calculator
from typing import *


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculators: Dict[int, calculator.Calculator] = {}
