from random import randint
from time import time

MAXSEQ = 4095
COUNTRYCODE_DEFAULT = "US"
OPMODE_DEFAULT = b"\x00"
COUNTRYOPERATIONS = 0


def _seedSeq():
    return randint(0, MAXSEQ)


class Agent:
    # useful for simplified calc of seq
    _seq: int

    # Frame control field first 4 bits set subtype, next two set type, followed by a version
    # by setting frame_control to 10000000, we are setting to Beacon v0 which is a subtype of
    # management frames
    frame_control: bytes = b"\x80"

    # Setting flags.
    # 0000 0000
    # |||| ||00  - DS status: from from STA to DS via an AP
    # |||| |0    - More fragments: this is the last fragment
    # |||| 0     - Retry: frame is not being retransmitted
    # |||0       - PWR MGT:: STA will stay up
    # ||0        - More Data: no more data buffered
    # |0         - Protected flag: Data is not protected
    # 0          - Order flag: Not strictly ordered
    flags: bytes = b"\x00"

    # Duration. Not meaningful in beacon (TBR)
    duration: bytes = b"\x00\x00"

    # Destination address. As this is beacon(broadcast), we set to 255 across the board
    dst: bytes = b"\xff\xff\xff\xff\xff\xff"

    # Source address. Important for children as we want this to be set within the range of the respective manufacturer's reserved range
    src: bytes = b"\x01\x02\x03\x04\x05\x06"
    # BSSID is used in beacons. Seems like we'll just set this to the same address as src (TBR)
    bssid: bytes = b"\x01\x02\x03\x04\x05\x06"

    # Sequence number is broke into the sequence number as the first 12 bits and fragment number in the last 4
    # this means that max value is 4095
    seq: bytes = b"\x00\x00"  # uint16le 2

    # timestamp in seconds. Might consider creating an artificial clockdrift
    timestamp_value: bytes = b"\x01\x02\x03\x04\x05\x06\x07\x08"

    # time in TUs (where 1 TU equals 1024microseconds). Setting to \x64\x00 is setting the intervale to 25600x1024/1000000 or ~26 seconds
    beacon_interval: bytes = b"\x64\x00"

    # advertize network capabilities
    # 0000 0000 0000 0101
    # |||| |||| |||| |||1    - ESS Bit. By setting to 1, we are claiming to be an access point
    # |||| |||| |||| ||0     - IBSS Bit. Mutally exclusive with ESS bit. Stations would set this to 1 and ESS to 0
    # |||| |||| |||| |1      - CF-Pollable. This particular configuration of the Contention-free polling bits means that the access point uses PCF for delivery but does not support polling
    # |||| |||| |||| 0       - CF-Poll request
    # |||| |||| |||0         - Privacy bit. WSetting to 1 requires use of WEP for confidentiality
    # |||| |||| ||0          - Short Preamble. Used in 802.11b to support high-rate DSSPHY. Setting it to 1 indicates that the network is using the short preamble
    # |||| |||| |0           - PBCC: Used in 802.11b to support high-rate DSSPHY.hen it is set to 1, it indicates that the network is using the packet binary convolution coding modulation scheme
    # |||| |||| 0            - Channel Agility. This field was added to 802.11b to support the high rate DSSS PHY. When it is set to one, it indicates that the network is using the Channel Agility option
    # |||| ||00              - Reserved
    # |||| |0                - Short slot time. This bit is set to one to indicate the use of the shorter slot time supported by 802.11g
    # |||0 0                 - Reserved
    # ||0                    - DSSS-OFDM This bit is set to one to indicate that the optional DSSS-OFDM frame construction in 802.11g is in use.
    #                       - Reserved
    capability_flags: bytes = b"\x00\x05"

    # SSID suggested generation ["Spark-","Mavic-"]+[random(abcdef0123456789) for i in range(6)]. This means that ssid length should always be 12 (\x0c)
    # SSID is 0-32 bytes plus 1 byte for field number and another for length (so value would be dynamically generated between 0-32)
    ssid: bytes = b"\x00\x0c\x41\x42\x43\x44\x45\x46\x41\x42\x43\x44\x45\x46"  # \x00+ssid.length.chr+ssid

    # up to 8 supported data rates should be encoded here. Each data rate is encoded as a byte, where 11 bits are for the data rate itself and the last bit is used for flagging if the rate is required or optional for connecting system
    # similar to ssid, first by is a field number and the following is the number of rates. As rates may change per platform, should be dynamically created
    supported_rates: bytes = b"\x82\x84\x8b\x0c\x12\x96\x18\x24"

    #Current channel being used. Assuming 2.4 Ghz, this should be between 0-14 (includes other country approved channels)
    # again, field id and length prefix
    current_channel: bytes = b"\x03\x01\x0b"  # last byte should be dynamic channel

    
    # explaination of this field is around letting stations know how many buffered packets are waiting to be picked up. Currently, because we are spoofing, this is statically set to 0, but we may want to add behavior to add realism
    #field id and length prefix
    traffic_indication_map: bytes = b"\x05\x04\x00\x01\x00\x00"
    
    #reglatory info about country of operation 

    # field id and length prefix
    #followed by a two bytes for a two letter country code
    #followed by a variable number of groupings of 3 bytes signifying the first(lowest) channel covered by the constrait, the number of channels covered, and the max power in dBm
    # there is an optional padding byte that should be added if the total length would be odd
    country_information: bytes = b"\x07\x06\x55\x53\x00\x01\x0b\x1e"


    erp_information: bytes = b"\x2a\x01\x00"
    extended_support_rates: bytes = b"\x32\x04\x30\x48\x60\x6c"
    ht_capabilities: bytes = b"\x2d\x1a\xac\x01\x02\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ht_information: bytes = b"\x3d\x16\x0b\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # third byte should be dynamic channel
    rsn_information: bytes = b"\x30\x14\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x0c\x00"
    vendor_specific_information: bytes = b"\xdd\x18\x00\x50\xf2\x02\x01\x01\x00\x00\x03\xa4\x00\x00\x27\xa4\x00\x00\x42\x43\x5e\x00\x62\x32\x2f\x00"

    def __init__(self,**kwargs):

        self._seq = randint(0, MAXSEQ)
        self._incrementseq()
        self._setCountryInfo()
        
        
    def _setCountryInfo(self,**kwargs):
        if  kwargs.get("country_code") is not None:
            country_code = kwargs["country_code"]
        else:
            country_code = COUNTRYCODE_DEFAULT
        if kwargs.get("op_mode") is not None:
            op_mode = ord(str(kwargs["op_mode"])).to_bytes(1,"little")
        else: 
            op_mode = OPMODE_DEFAULT
        if kwargs.get("country_regs") is not None:
            country_regs = kwargs["country_regs"]
        else:
            country_regs = b"\x01\x0b\x1e"
        country_postfix = b''.join([ord(str(val).upper()).to_bytes(1,"little") for val in country_code])+op_mode+country_regs
        
        #if length is not even, add padding trailer. Pretty sure new length is calculated TBR
        if len(country_postfix)%2 != 0:
            country_postfix = country_postfix+b"\x00"



        self.country_information = b'\x07'+len(country_postfix).to_bytes(1,"little")+ country_postfix

    def _incrementseq(self):
        self._seq = self._seq + 1
        if self._seq > MAXSEQ:
            self._seq = 0
        # Recall, first 12 bits are, last four are fragment(which should always be 0)
        self.seq = (self._seq << 4).to_bytes(2, "little")

    def get_bytes(self):

        """
        Get the bytestring for sending. Should produce 128byte array ALWAYS
        Note for optimizing - allocate the byte array once within __init__ and then just update the portions of the array as needed
        """
        out = [
            self.frame_control,
            self.flags,
            self.duration,
            self.dst,
            self.src,
            self.bssid,
            self.seq,
            self.timestamp_value,
            self.beacon_interval,
            self.capability_flags,
            b"\x00",#adding addiditional bytes required to handle dynamic ssid assigned (i.e calculating len at runtime)
            len(self.ssid).to_bytes(1,"little"),
            self.ssid,
            b"\x01",
            len(self.supported_rates).to_bytes(1,"little"),
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
            self.timestamp_value = int(time()).to_bytes(8, "little")

            yield b"".join(out)

    def get_packet(self) -> bytes:
        return next(self.get_bytes())
