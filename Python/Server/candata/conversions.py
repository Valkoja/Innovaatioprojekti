from collections import namedtuple
from struct import unpack, pack


class XSiteDecoder:
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
            ('0x60A', ('<3xf', namedtuple('slope', 'slope')))
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
            format = self._pdo_map[_id]
            msg = format[1]._make(unpack(format[0], data))
            self._ok = self._ok + 1
            if type(msg).__name__.endswith('quaternion'):
                return format[1]._make([
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
        padding = 4
        _id = f"{id:#0{padding}x}".lower()
        if _id in self._sdo_map:
            format = self._sdo_map[_id]
            msg = format[1]._make(unpack(format[0], data))
            self._ok = self._ok + 1
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
                  id=0x60A, data=[0b00101111, 0x20, 0x20, 0x02, 0x01, 0x0, 0x0, 0x0])),
            ('set_slope',
             dict(format=namedtuple('set_slope', 'id data'),
                  id=0x58A, data=[0b00101111, 0x20, 0x20, 0x01], input_transform=lambda arg: pack('<f', arg))),
            ('get_slope',
             dict(format=namedtuple('get_slope', 'id data'),
                id=0x60A, data=[0b01000000, 0x20, 0x20, 0x01, 0x0, 0x0, 0x0, 0x0])),
        ])
        self._ok = 0
        self._failed = 0

    def encode_sdo(self, command, argument=None):
        if command in self._sdo_map:
            fmt = self._sdo_map[command]
            if argument:
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
