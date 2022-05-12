import pathlib
from json import load
from math import pi


print("loading mac addresses")

macaddresses = {}
with open(
    pathlib.Path(__file__).parent.resolve().as_posix() + "/agents/macs.json"
) as f:
    macaddresses = load(f)
print(macaddresses)


def getMAC(company: str) -> bytes:
    pass


def latlon_format(val: float) -> int:
    """
    Converting to radians and multiplying by 10000000
    returns (val/180)*PI*10000000
    """
    return int((val / 180.0) * pi * 10000000)
