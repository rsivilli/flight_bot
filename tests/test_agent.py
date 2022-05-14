from flight_bot.agents.agent import Agent


def test_init():
    assert Agent() is not None


def test_toBytres():
    agent = Agent()
    assert len(agent.get_packet()) == 186


def test_difseq():
    agent1 = Agent()
    agent2 = Agent()
    assert agent1.seq != agent2.seq