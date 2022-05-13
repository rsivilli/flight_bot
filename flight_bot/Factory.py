from enum import Enum

from flight_bot.agents.agent import Agent
from flight_bot.agents.dji import DJI_Base
from flight_bot.agents.parrot import Parrot_Base


class DroneType(Enum):
    """Supported drone types for agent create"""
    Base = 1
    DJI = 2
    PARROT = 3


def getDrone(dronetype: DroneType) -> Agent:
    if dronetype == DroneType.DJI:
        return DJI_Base()
    elif dronetype == DroneType.PARROT:
        return Parrot_Base()
    elif dronetype == DroneType.Base:
        return Agent()
