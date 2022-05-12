from flight_bot.agents.dji import DJI_Base


def test_base():
    assert DJI_Base() is not None


def test_tobytes():
    agent = DJI_Base()
    assert len(agent.get_bytes()) == 270
