from math import pi
from random import randint

MAXSEQ = 65535


def _seedSeq():
    return randint(0, MAXSEQ)


class Agent:
    _seq: int
    agent_type: bytes = b"\x80"
    flags: bytes = b"\x00"
    duration: bytes = b"\x00\x00"
    dst: bytes = b"\xff\xff\xff\xff\xff\xff"
    src: bytes = b"\x01\x02\x03\x04\x05\x06"  # Set this to MAC address. Pull from drone
    bssid: bytes = b"\x01\x02\x03\x04\x05\x06"
    seq: bytes = b"\x00\x00"  # uint16le 2
    timestamp_value: bytes = b"\x01\x02\x03\x04\x05\x06\x07\x08"  # this is probably
    beacon_interval: bytes = b"\x64\x00"
    capability_flags: bytes = b"\x00\x05"

    # SSID suggested generation ["Spark-","Mavic-"]+[random(abcdef0123456789) for i in range(6)]. This means that ssid length should always be 12 (\x0c)
    ssid: bytes = b"\x00\x0c\x41\x42\x43\x44\x45\x46\x41\x42\x43\x44\x45\x46"  # \x00+ssid.length.chr+ssid
    supported_rates: bytes = b"\x01\x08\x82\x84\x8b\x0c\x12\x96\x18\x24"
    current_channel: bytes = b"\x03\x01\x0b"  # last byte should be dynamic channel
    traffic_indication_map: bytes = b"\x05\x04\x00\x01\x00\x00"
    country_information: bytes = b"\x07\x06\x55\x53\x00\x01\x0b\x1e"
    erp_information: bytes = b"\x2a\x01\x00"
    extended_support_rates: bytes = b"\x32\x04\x30\x48\x60\x6c"
    ht_capabilities: bytes = b"\x2d\x1a\xac\x01\x02\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ht_information: bytes = b"\x3d\x16\x0b\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # third byte should be dynamic channel
    rsn_information: bytes = b"\x30\x14\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x0c\x00"
    vendor_specific_information: bytes = b"\xdd\x18\x00\x50\xf2\x02\x01\x01\x00\x00\x03\xa4\x00\x00\x27\xa4\x00\x00\x42\x43\x5e\x00\x62\x32\x2f\x00"

    def __init__(self):
        self._seq = randint(0, MAXSEQ)
        self._incrementseq()

    def _incrementseq(self):
        self._seq = self._seq + 1
        if self._seq > MAXSEQ:
            self._seq = 0
        self.seq = self._seq.to_bytes(2, "little")

    def get_bytes(self):

        """
        Get the bytestring for sending. Should produce 128byte array ALWAYS
        Note for optimizing - allocate the byte array once within __init__ and then just update the portions of the array as needed
        """
        out = [
            self.agent_type,
            self.flags,
            self.duration,
            self.dst,
            self.src,
            self.bssid,
            self.seq,
            self.timestamp_value,
            self.beacon_interval,
            self.capability_flags,
            self.ssid,
            self.supported_rates,
            self.current_channel,
            self.traffic_indication_map,
            self.country_information,
            self.erp_information,
            self.extended_support_rates,
            self.ht_capabilities,
            self.ht_information,
            self.rsn_information,
            self.vendor_specific_information,
        ]
        while True:
            self._incrementseq()

            yield b"".join(out)

    def get_packet(self) -> bytes:
        return next(self.get_bytes())
