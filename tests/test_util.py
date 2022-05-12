from flight_bot.util import getMAC


import pathlib
from json import load 

macaddresses = {}
with open(
    pathlib.Path(__file__).parent.resolve().as_posix() + "/../flight_bot/agents/macs.json"
) as f:
    macaddresses = load(f)
def checkmac(mac:bytes,company:str):
    macstring = mac.hex()
    for mac_base in macaddresses[company]:
        print("checking {} against {}".format(macstring,mac_base))
        if macstring.find(mac_base.lower()) > -1:
            return True
    return False

def test_mac_basic():
    for company in ["parrot","dji"]:
        mac = getMAC(company=company)
        assert type(mac) == bytes
        assert len(mac) == 6
        assert checkmac(mac,company)
        