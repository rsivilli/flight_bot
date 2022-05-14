from flight_bot.agents.agent import Agent
from flight_bot.util import getMAC


class Parrot_Base(Agent):
    def __init__(self):
        super().__init__()
        self.src = getMAC("parrot")
