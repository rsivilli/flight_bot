from flight_bot.agents.agent import Agent
from pydantic import conbytes
from flight_bot.util import getMAC

class Parrot_Base(Agent):
    src: conbytes(
        max_length=6, min_length=6
    ) = getMAC("parrot")
    def __init__(self):
        super().__init__()
