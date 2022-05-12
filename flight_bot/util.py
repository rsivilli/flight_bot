import pathlib
from json import load
from math import pi
import random
import string


print("loading mac addresses")

macaddresses = {}
with open(
    pathlib.Path(__file__).parent.resolve().as_posix() + "/agents/macs.json"
) as f:
    macaddresses = load(f)
print(macaddresses)


def getMAC(company: str) -> bytes:
    reservedmacs = list(macaddresses.get(company).keys())
    macbase = str(random.choice(reservedmacs)).lower()
    print(macbase)
    while(len(macbase)<12):
        macbase = macbase+str(random.choice(string.hexdigits)).lower()
    print(macbase)
    print(bytes.fromhex(macbase))
    return bytes.fromhex(macbase)


def latlon_format(val: float) -> int:
    """
    Converting to radians and multiplying by 10000000
    returns (val/180)*PI*10000000
    """
    return int((val / 180.0) * pi * 10000000)
