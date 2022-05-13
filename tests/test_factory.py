from flight_bot.agents.agent import Agent
from flight_bot.agents.dji import DJI_Base
from flight_bot.agents.parrot import Parrot_Base
from flight_bot.factory import DroneType
from flight_bot.factory import getDrone


def test_base():
    """make sure factory gives us what we're asking for"""
    assert type(getDrone(DroneType.Base)) == Agent
    assert type(getDrone(DroneType.DJI)) == DJI_Base
    assert type(getDrone(DroneType.PARROT)) == Parrot_Base
