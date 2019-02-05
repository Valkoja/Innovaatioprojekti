import time
import datetime
from pathlib import Path
import sys
from conversions import PDODecoder

# Play busmaster logs
class LogPlayer():
    def processFile(self, file, reactor, callback, ignoreFailed=True):
        recorded_start_time = None
        decoder = PDODecoder()
        file_in = Path(file)

        with open(file_in, 'r') as input:
            for line in input:
                if line.startswith('***'):
                    continue
                fields = line.split(' ')

                # Do maths to get proper times for replay
                timestring = fields[0]
                # Busmaster timestamp format 16:21:32:6459
                timestamp = datetime.datetime.strptime(timestring, '%H:%M:%S:%f').timestamp()

                if recorded_start_time is None:
                    recorded_start_time = timestamp
                remaining_gap = timestamp - recorded_start_time

                id = fields[3][2:]
                data = ''.join(fields[6:-1])
                message = decoder.decode_pdo(int(id, 16), bytes.fromhex(data))

                if message:
                    reactor.callLater(remaining_gap, callback, message)