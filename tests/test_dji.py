from flight_bot.agents.dji import DJI_Base


def test_base():
    assert DJI_Base() is not None


def test_toBytes():
    agent = DJI_Base()
    assert len(agent.get_packet()) == 270


def test_diffMacandSeq():
    agent1 = DJI_Base()
    agent2 = DJI_Base()

    assert agent1.seq != agent2.seq
    assert agent1.src != agent2.src
