from collections import namedtuple
from struct import unpack, pack


class XSiteDecoder:
    SDO_RECEIVE_ID = int('0x58a', 16)

    def __init__(self):
        self._pdo_map = dict([
            ('0x181', ('<7?', namedtuple('limit_warnings', 'left right upper lower forward property overload'))),
            ('0x184', ('<2f', namedtuple('zero_level_1', 'height_from_zero distance_to_zero'))),
            ('0x185', ('<f', namedtuple('zero_level_2', 'height_to_slope_from_zero'))),
            ('0x188', ('<4h', namedtuple('angles_1', 'main_boom digging_arm bucket heading'))),
            ('0x189', ('<2h', namedtuple('angles_2', 'frame_pitch frame_roll'))),
            ('0x18b', ('<4h', namedtuple('frame_orientation_quaternion', 'w x y z'))),
            ('0x18c', ('<4h', namedtuple('main_boom_orientation_quaternion', 'w x y z'))),
            ('0x18d', ('<4h', namedtuple('digging_arm_orientation_quaternion', 'w x y z'))),
            ('0x18e', ('<4h', namedtuple('bucket_orientation_quaternion', 'w x y z')))
        ])
        self._sdo_map = dict([
            ('0x430x20200x1', ('<f', namedtuple('slope', 'slope'))), # 0x43 0x20 0x20 0x1 <-> 43 20 20 01 00 00 00 00
            ('0x600x20200x2', ('<i', namedtuple('zero_with_bucket_tip', 'result'))), # 0x60 0x20 0x20 0x1 <-> 60 20 20 01 00 00 00 00
            ('0x600x20200x1', ('<i', namedtuple('set_slope', 'result'))) # 0x60 0x20 0x20 0x2 <-> 60 20 20 02 00 00 00 00
        ])
        self._ok = 0
        self._failed = 0

    # PDO: id+message, in bytes
    def decode_pdo(self, id, data):
        if not isinstance(id, int):
            raise TypeError
        if not (isinstance(data, bytes) or isinstance(data, bytearray)):
            raise TypeError
        padding = 4
        _id = f"{id:#0{padding}x}".lower()
        if _id in self._pdo_map:
            msgformat = self._pdo_map[_id]
            msg = msgformat[1]._make(unpack(msgformat[0], data))
            self._ok = self._ok + 1
            if type(msg).__name__.endswith('quaternion'):
                return msgformat[1]._make([
                    XSiteDecoder.qToFloat(msg.w, 14),
                    XSiteDecoder.qToFloat(msg.x, 14),
                    XSiteDecoder.qToFloat(msg.y, 14),
                    XSiteDecoder.qToFloat(msg.z, 14)
                ])
            return msg
        else:
            self._failed = self._failed + 1
            return False

    # SDO: id+message, in bytes
    def decode_sdo(self, id, data):
        if not isinstance(id, int):
            raise TypeError
        if not (isinstance(data, bytes) or isinstance(data, bytearray)):
            raise TypeError
        if id == XSiteDecoder.SDO_RECEIVE_ID:
        # if id == 1418:
            sdoformat = '<bhb'
            sdoaddress = namedtuple('sdo', 'status index subindex')._make(unpack(sdoformat, data[0:4]))
            sdoid = hex(sdoaddress.status) + hex(sdoaddress.index) + hex(sdoaddress.subindex)
            if sdoid in self._sdo_map:
                msgformat = self._sdo_map[sdoid]
                msg = msgformat[1]._make(unpack(msgformat[0], data[-4:]))
                self._ok = self._ok + 1
                print(msg)
                return msg
            else:
                self._failed = self._failed + 1
                return False

    @classmethod
    def qToFloat(cls, q, fraction):
        if q != 0:
            return float(q) * 2 ** -fraction
        else:
            return float(0)

    def ok_parses(self):
        return self._ok

    def fail_parses(self):
        return self._failed


# Message that zeroes 2D-features at bucket tip
# ID is SDO download channel for node 0
# Data bytes:
# SDO expedited download
# Index of 2D-features, 0x2020
# Subindex of zero with bucket tip, 0x02
# "Writing" 1 into that register

# Message that sets 2D-features 'slope'
# ID is SDO download channel for node 0
# Data bytes:
# SDO expedited download
# Index of 2D-features, 0x2020
# Subindex of zero with bucket tip, 0x01
# "Writing" argument into that register

# Message that reads 2D-features 'slope'
# ID is SDO upload channel for node 0
# Data bytes:
# SDO expedited upload
# Index of 2D-features, 0x2020
# Subindex of zero with bucket tip, 0x01
# "Reading" value of that register
# Requires implementation of SDODecoder as well...

class SDOEncoder:
    def __init__(self):
        self._sdo_map = dict([
            ('zero_with_bucket_tip',
             dict(format=namedtuple('zero_with_bucket_tip', 'id data'),
                  id=0x60A, data=[0b00101111, 0x20, 0x20, 0x02, 0x01, 0x0, 0x0, 0x0])), # 60 20 20 02 00 00 00 00
            ('set_slope',
             dict(format=namedtuple('set_slope', 'id data'),
                  id=0x60A, data=[0b00100011, 0x20, 0x20, 0x01], input_transform=lambda arg: pack('<f', arg))), # 60 20 20 01 00 00 00 00
            ('get_slope',
             dict(format=namedtuple('get_slope', 'id data'),
                id=0x60A, data=[0b01000000, 0x20, 0x20, 0x01, 0x0, 0x0, 0x0, 0x0])), # 43 20 20 01 00 00 00 00
        ])
        self._ok = 0
        self._failed = 0

    def encode_sdo(self, command, argument=None):
        if command in self._sdo_map:
            fmt = self._sdo_map[command]
            if argument is not None:
                data = fmt['data'].copy()
                data.extend(fmt['input_transform'](argument))
                sdo = fmt['format'](fmt['id'], data)
            else:
                data = fmt['data']
                sdo = fmt['format'](fmt['id'], data)
            self._ok = self._ok + 1
            return sdo
        else:
            self._failed = self._failed + 1
            return False

    def ok_parses(self):
        return self._ok

    def fail_parses(self):
        return self._failed
