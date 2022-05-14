from time import sleep

from flight_bot.agents.agent import Agent
from flight_bot.agents.agent import MAXSEQ


def test_init():
    assert Agent() is not None


def test_toBytres():
    agent = Agent()
    assert len(agent.get_packet()) == 186


def test_diffSeq():
    agent1 = Agent()
    agent2 = Agent()
    assert agent1.seq != agent2.seq


def test_incrementSeq():
    agent1 = Agent()
    time1 = agent1._seq
    agent1.get_packet()
    time2 = agent1._seq
    assert time1 + 1 == time2 or (time2 == 0 and time1 > time2)


def test_incrementRollover():
    agent1 = Agent()
    agent1._seq = MAXSEQ
    agent1.get_packet()
    assert agent1._seq == 0


def test_diffPacket():
    agent = Agent()
    assert agent.get_packet() != agent.get_packet()


def test_timestampUpdating():
    agent = Agent()
    agent.get_packet()
    time1 = agent.timestamp_value
    sleep(1)
    agent.get_packet()
    time2 = agent.timestamp_value
    assert time2 > time1
