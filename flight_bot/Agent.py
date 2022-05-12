
from pydantic import BaseModel,conbytes,constr,conint
from math import pi


def latlon_format(val:float)->int:
    '''
    Converting to radians and multiplying by 10000000 
    returns (val/180)*PI*10000000
    '''
    return (int((val/180.0)*pi*10000000))

class Agent(BaseModel):
    agent_type:conbytes(max_length=1,min_length=1) = b'\x80'
    flags:conbytes(max_length=1,min_length=1) = b'\x00'
    duration:conbytes(max_length=2,min_length=2) = b'\x00\x00'
    dst:conbytes(max_length=6,min_length=6) = b'\xff\xff\xff\xff\xff\xff'
    src:conbytes(max_length=6,min_length=6) = b'\x01\x02\x03\x04\x05\x06' #src seems to always equal bssid
    bssid:conbytes(max_length=6,min_length=6) = b'\x01\x02\x03\x04\x05\x06'
    seq:conbytes(max_length=2,min_length=2)= b'\x01\x02'
    timestamp_value:conbytes(max_length=8,min_length=8) = b'\x01\x02\x03\x04\x05\x06\x07\x08' #this is probably uint8le
    beacon_interval:conbytes(max_length=2,min_length=2) = b'\x64\x00'
    capability_flags:conbytes(max_length=2,min_length=2) = b'\x00\x05'

    #SSID suggested generation ["Spark-","Mavic-"]+[random(abcdef0123456789) for i in range(6)]. This means that ssid length should always be 12 (\x0c)
    ssid:conbytes(max_length=14,min_length=14) = b'\x00\x0c\x41\x42\x43\x44\x45\x46\x41\x42\x43\x44\x45\x46' #\x00+ssid.length.chr+ssid 
    supported_rates:conbytes(max_length=10,min_length=10) = b'\x01\x08\x82\x84\x8b\x0c\x12\x96\x18\x24'
    current_channel:conbytes(max_length=3,min_length=3)= b'\x03\x01\x0b' #last byte should be dynamic channel
    traffic_indication_map:conbytes(max_length=6,min_length=6) = b'\x05\x04\x00\x01\x00\x00'
    country_information:conbytes(max_length=8,min_length=8) = b'\x07\x06\x55\x53\x00\x01\x0b\x1e'
    erp_information:conbytes(max_length=3,min_length=3) = b'\x2a\x01\x00'
    extended_support_rates:conbytes(max_length=6,min_length=6) = b'\x32\x04\x30\x48\x60\x6c'
    ht_capabilities:conbytes(max_length=28,min_length=28) = b'\x2d\x1a\xac\x01\x02\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ht_information:conbytes(max_length=24,min_length=24)  = b'\x3d\x16\x0b\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' #third byte should be dynamic channel
    rsn_information:conbytes(max_length=22,min_length=22) = b'\x30\x14\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x0c\x00'
    vendor_specific_information:conbytes(max_length=26,min_length=26) = b'\xdd\x18\x00\x50\xf2\x02\x01\x01\x00\x00\x03\xa4\x00\x00\x27\xa4\x00\x00\x42\x43\x5e\x00\x62\x32\x2f\x00'
    
    header:conbytes(max_length=8,min_length=8) = b'\xdd\x52\x26\x37\x12\x58\x62\x13' #uint64le 8
    sub_cmd:conbytes(min_length=1,max_length=1) = b'\x10' #uint8 1
    ver:conbytes(min_length=1,max_length=1) =b'\x01'#uint8 1
    seq:conint(le=65535,ge=0) = 90 #uint16le 2
    state_info:conbytes(min_length=2,max_length=2) = b"\xD7\x0F" #uint16le 2 Just seems to be statically set?
    sn:conbytes(min_length=16,max_length=16) = b"DroneID is crap!"  #string len(16) 16. It just so happens that statement fits in the 16byte requirement for an id
    
    #Picked a random place in the general RU area
    latitude:conint(le=2147483647,ge=-2147483648) = latlon_format(55.750446)#int32le 4. Original code is starting in deg N, converting to radians and multiplying by 10000000 (lat/180)*PI*10000000
    longitude:conint(le=2147483647,ge=-2147483648) = latlon_format(37.617494)#int32le 4. Original code is starting in deg E converting to radians and multiplying by 10000000 (lat/180)*PI*10000000

    altitude:conint(le=2147483647,ge=-2147483648) = 0 #int16le 2
    height:conint(le=32767,ge=-32768 ) = 0 #int16le 2 
    v_north:conint(le=32767,ge=-32768 ) = 0 #int16le 2 
    v_east:conint(le=32767,ge=-32768 ) = 0 #int16le 2
    v_up:conint(le=32767,ge=-32768 ) = 0 #int16le 2
    pitch:conint(le=32767,ge=-32768 ) = 0 #int16le 2
    roll:conint(le=32767,ge=-32768 ) = 0 #int16le 2
    yaw:conint(le=32767,ge=-32768 ) = 0  #int16le 2

    #picked random place in the general CN area
    latitude_home:conint(le=2147483647,ge=-2147483648) = latlon_format(22.537021) #int32le 4
    longitude_home:conint(le=2147483647,ge=-2147483648)= latlon_format(113.952322) #int32le 4


    product_type:conint(le=255,ge=0) = 10#uint8 1
    uuid_len:conint(le=255,ge=0) = 6 #uint8 1. So this is weird, but it seems that the drone id is 6 characters with a trailer of 14 0s
    uuid:constr(min_length=20,max_length=20) = b'yesyes'+b'\x00'*14 #str len(20) 20
    

    
    def get_bytes(self)->bytes:
        """
        Get the bytestring for sending. Should produce 128byte array ALWAYS
        Note for optimizing - allocate the byte array once within __init__ and then just update the portions of the array as needed
        """
        out = [self.agent_type
        ,self.flags
        ,self.duration
        ,self.dst
        ,self.src
        ,self.bssid
        ,self.seq.to_bytes(2,'little')
        ,self.timestamp_value
        ,self.beacon_interval
        ,self.capability_flags
        ,self.ssid
        ,self.supported_rates
        ,self.current_channel
        ,self.traffic_indication_map
        ,self.country_information
        ,self.erp_information
        ,self.extended_support_rates
        ,self.ht_capabilities
        ,self.ht_information
        ,self.rsn_information
        ,self.vendor_specific_information
        ,self.header
        ,self.sub_cmd
        ,self.ver
        ,self.seq.to_bytes(2,'little')
        ,self.state_info
        ,self.sn
        ,self.latitude.to_bytes(4,'little')
        ,self.longitude.to_bytes(4,'little')
        ,self.altitude.to_bytes(2,'little')
        ,self.height.to_bytes(2,'little')
        ,self.v_north.to_bytes(2,'little')
        ,self.v_east.to_bytes(2,'little')
        ,self.v_up.to_bytes(2,'little')
        ,self.pitch.to_bytes(2,'little')
        ,self.roll.to_bytes(2,'little')
        ,self.yaw.to_bytes(2,'little')
        ,self.latitude_home.to_bytes(4,'little')
        ,self.longitude_home.to_bytes(4,'little')
        ,self.product_type.to_bytes(1,'little')
        ,self.uuid_len.to_bytes(1,'little')
        ,self.uuid]
        print(out)
        for val in out:
            print("{}:{}".format(val,len(val)))
        print(sum([len(val) for val in out]))
            



        return b"".join(out)
        



