from collections import namedtuple
from struct import unpack

class PDODecoder():
    def __init__(self):
        self._pdo_map = dict([
            ('0x181', ('<7?', namedtuple('limit_warnings', 'left right upper lower forward property overload'))),
            ('0x184', ('<2f', namedtuple('zero_level_1', 'height_from_zero distance_to_zero'))),
            ('0x185', ('<f', namedtuple('zero_level_2', 'height_to_slope_from_zero'))),
            ('0x188', ('<4h', namedtuple('angles_1', 'main_boom digging_arm bucket heading'))),
            ('0x189', ('<2h', namedtuple('angles_2', 'frame_pitch frame_roll'))),
            ('0x18b', ('<4h', namedtuple('frame_orientation_quarternion', 'w x y z'))),
            ('0x18c', ('<4h', namedtuple('main_boom_orientation_quarternion', 'w x y z'))),
            ('0x18d', ('<4h', namedtuple('digging_arm_orientation_quarternion', 'w x y z'))),
            ('0x18e', ('<4h', namedtuple('bucket_orientation_quarternion', 'w x y z')))
        ])
        self._ok = 0
        self._failed = 0

    #PDO: id+message, in bytes
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
            if type(msg).__name__.endswith('quarternion'):
                return format[1]._make([PDODecoder.qToFloat(msg.w, 14), PDODecoder.qToFloat(msg.x, 14), PDODecoder.qToFloat(msg.y, 14), PDODecoder.qToFloat(msg.z, 14)])
            return msg
        else:
            self._failed = self._failed + 1
            return False
            
    @classmethod  
    def qToFloat(self, q, fraction):
        if q != 0:
            return float(q) * 2 ** -fraction
        else:
            return float(0)
    
    def ok_parses(self):
        return self._ok
    
    def fail_parses(self):
        return self._failed