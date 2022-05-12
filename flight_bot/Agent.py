
from pydantic import BaseModel,conbytes,constr,conint

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
    state_info:conbytes(min_length=2,max_length=2) = "\xD7\x0F" #uint16le 2
    sn:constr(min_length=16,max_length=16) #string len(16) 16
    latitude:conint(le=2147483647,ge=-2147483648) #int32le 4
    longitude:conint(le=2147483647,ge=-2147483648) #int32le 4
    altitude:conint(le=2147483647,ge=-2147483648) #int16le 2
    height:conint(le=32767,ge=-32768 ) #int16le 2 
    v_north:conint(le=32767,ge=-32768 ) #int16le 2 
    v_east:conint(le=32767,ge=-32768 ) #int16le 2
    v_up:conint(le=32767,ge=-32768 ) #int16le 2
    pitch:conint(le=32767,ge=-32768 ) #int16le 2
    roll:conint(le=32767,ge=-32768 ) #int16le 2
    yaw:conint(le=32767,ge=-32768 ) #int16le 2
    latitude_home:conint(le=2147483647,ge=-2147483648) #int32le 4
    longitude_home:conint(le=2147483647,ge=-2147483648) #int32le 4
    product_type:conint(le=255,ge=0) #uint8 1
    uuid_len:conint(le=255,ge=0) #uint8 1
    uuid:constr(min_length=20,max_length=20) #str len(20) 20

    def get_bytes(self)->bytes:
        """
        Get the bytestring for sending. Should produce 128byte array ALWAYS
        Note for optimizing - allocate the byte array once within __init__ and then just update the portions of the array as needed
        """
        out = bytearray()
        out.append(self.agent_type)
        out.append(self.flags)
        out.append(self.duration)
        out.append(self.dst)
        out.append(self.src)
        out.append(self.bssid)
        out.append(self.seq)
        out.append(self.timestamp_value)
        out.append(self.beacon_interval)
        out.append(self.capability_flags)
        out.append(self.ssid)
        out.append(self.supported_rates)
        out.append(self.current_channel)
        out.append(self.traffic_indication_map)
        out.append(self.country_information)
        out.append(self.erp_information)
        out.append(self.extended_support_rates)
        out.append(self.ht_capabilities)
        out.append(self.ht_information)
        out.append(self.rsn_information)
        out.append(self.vendor_specific_information)
        out.append(self.header)
        out.append(self.sub_cmd)
        out.append(self.ver)
        out.append(self.seq)
        out.append(self.state_info)
        out.append(self.sn)
        out.append(self.latitude.to_bytes(4,'little'))
        out.append(self.longitude.to_bytes(4,'little'))
        out.append(self.altitude.to_bytes(2,'little'))
        out.append(self.height.to_bytes(2,'little'))
        out.append(self.v_north.to_bytes(2,'little'))
        out.append(self.v_east.to_bytes(2,'little'))
        out.append(self.v_up.to_bytes(2,'little'))
        out.append(self.pitch.to_bytes(2,'little'))
        out.append(self.roll.to_bytes(2,'little'))
        out.append(self.yaw.to_bytes(2,'little'))
        out.append(self.latitude_home.to_bytes(4,'little'))
        out.append(self.longitude_home.to_bytes(4,'little'))
        out.append(self.product_type.to_bytes(1,'little'))
        out.append(self.uuid_len.to_bytes(1,'little'))
        out.append(self.uuid)



        return out
        



