from pydantic import conbytes
from pydantic import conint
from pydantic import constr

from flight_bot.agents.agent import Agent
from flight_bot.util import getMAC
from flight_bot.util import latlon_format


class DJI_Base(Agent):
    # Begin DJI specific info
    header: bytes = b"\xdd\x52\x26\x37\x12\x58\x62\x13"  # uint64le 8
    sub_cmd: bytes = b"\x10"  # uint8 1
    ver: bytes = b"\x01"  # uint8 1
    state_info: bytes = b"\xD7\x0F"  # uint16le 2 Just seems to be statically set?
    sn: bytes = b"DroneID is crap!"  # string len(16) 16. It just so happens that statement fits in the 16byte requirement for an id

    # Picked a random place in the general RU area
    latitude: int = latlon_format(
        55.750446
    )  # int32le 4. Original code is starting in deg N, converting to radians and multiplying by 10000000 (lat/180)*PI*10000000
    longitude: int = latlon_format(
        37.617494
    )  # int32le 4. Original code is starting in deg E converting to radians and multiplying by 10000000 (lat/180)*PI*10000000

    altitude: int = 0  # int16le 2
    height: int = 0  # int16le 2
    v_north: int = 0  # int16le 2
    v_east: int = 0  # int16le 2
    v_up: int = 0  # int16le 2
    pitch: int = 0  # int16le 2
    roll: int = 0  # int16le 2
    yaw: int = 0  # int16le 2

    # picked random place in the general CN area
    latitude_home: int = latlon_format(22.537021)  # int32le 4
    longitude_home: int = latlon_format(113.952322)  # int32le 4

    product_type: int = 10  # uint8 1
    uuid_len: int = 6  # uint8 1. So this is weird, but it seems that the drone id is 6 characters with a trailer of 14 0s
    uuid: bytes = b"yesyes" + b"\x00" * 14  # str len(20) 20

    def __init__(self):
        super().__init__()
        self.src = getMAC("dji")
        self.bssid = self.src

    def get_packet(self) -> bytes:
        additional = b"".join(
            [
                self.header,
                self.sub_cmd,
                self.ver,
                self.seq,
                self.state_info,
                self.sn,
                self.latitude.to_bytes(4, "little"),
                self.longitude.to_bytes(4, "little"),
                self.altitude.to_bytes(2, "little"),
                self.height.to_bytes(2, "little"),
                self.v_north.to_bytes(2, "little"),
                self.v_east.to_bytes(2, "little"),
                self.v_up.to_bytes(2, "little"),
                self.pitch.to_bytes(2, "little"),
                self.roll.to_bytes(2, "little"),
                self.yaw.to_bytes(2, "little"),
                self.latitude_home.to_bytes(4, "little"),
                self.longitude_home.to_bytes(4, "little"),
                self.product_type.to_bytes(1, "little"),
                self.uuid_len.to_bytes(1, "little"),
                self.uuid,
            ]
        )
        return super().get_packet() + additional
