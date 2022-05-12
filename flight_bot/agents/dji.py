from pydantic import conbytes
from pydantic import conint
from pydantic import constr

from flight_bot.agents.agent import Agent
from flight_bot.util import latlon_format


class DJI_Base(Agent):
    # Begin DJI specific info
    header: conbytes(
        max_length=8, min_length=8
    ) = b"\xdd\x52\x26\x37\x12\x58\x62\x13"  # uint64le 8
    sub_cmd: conbytes(min_length=1, max_length=1) = b"\x10"  # uint8 1
    ver: conbytes(min_length=1, max_length=1) = b"\x01"  # uint8 1
    seq: conint(le=65535, ge=0) = 90  # uint16le 2
    state_info: conbytes(
        min_length=2, max_length=2
    ) = b"\xD7\x0F"  # uint16le 2 Just seems to be statically set?
    sn: conbytes(
        min_length=16, max_length=16
    ) = b"DroneID is crap!"  # string len(16) 16. It just so happens that statement fits in the 16byte requirement for an id

    # Picked a random place in the general RU area
    latitude: conint(le=2147483647, ge=-2147483648) = latlon_format(
        55.750446
    )  # int32le 4. Original code is starting in deg N, converting to radians and multiplying by 10000000 (lat/180)*PI*10000000
    longitude: conint(le=2147483647, ge=-2147483648) = latlon_format(
        37.617494
    )  # int32le 4. Original code is starting in deg E converting to radians and multiplying by 10000000 (lat/180)*PI*10000000

    altitude: conint(le=2147483647, ge=-2147483648) = 0  # int16le 2
    height: conint(le=32767, ge=-32768) = 0  # int16le 2
    v_north: conint(le=32767, ge=-32768) = 0  # int16le 2
    v_east: conint(le=32767, ge=-32768) = 0  # int16le 2
    v_up: conint(le=32767, ge=-32768) = 0  # int16le 2
    pitch: conint(le=32767, ge=-32768) = 0  # int16le 2
    roll: conint(le=32767, ge=-32768) = 0  # int16le 2
    yaw: conint(le=32767, ge=-32768) = 0  # int16le 2

    # picked random place in the general CN area
    latitude_home: conint(le=2147483647, ge=-2147483648) = latlon_format(
        22.537021
    )  # int32le 4
    longitude_home: conint(le=2147483647, ge=-2147483648) = latlon_format(
        113.952322
    )  # int32le 4

    product_type: conint(le=255, ge=0) = 10  # uint8 1
    uuid_len: conint(
        le=255, ge=0
    ) = 6  # uint8 1. So this is weird, but it seems that the drone id is 6 characters with a trailer of 14 0s
    uuid: constr(min_length=20, max_length=20) = (
        b"yesyes" + b"\x00" * 14
    )  # str len(20) 20

    def get_bytes(self) -> bytes:
        additional = b"".join(
            [
                self.header,
                self.sub_cmd,
                self.ver,
                self.seq.to_bytes(2, "little"),
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
        return super().get_bytes() + additional
