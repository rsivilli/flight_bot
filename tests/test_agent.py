from flight_bot.agents.agent import Agent


def test_init():
    assert Agent() is not None


def test_toBytres():
    agent = Agent()
    assert len(agent.get_bytes()) == 186
