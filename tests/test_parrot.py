from flight_bot.agents.parrot import Parrot_Base


def test_base():
    """Make sure class is not breaking in some way"""
    assert Parrot_Base() is not None


def test_tobytes():
    """Parrot does not add to broadcast base. Should be the same length as base agent"""
    agent = Parrot_Base()
    assert len(agent.get_packet()) == 188
