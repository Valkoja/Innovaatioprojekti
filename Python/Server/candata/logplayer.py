import time
import datetime
from pathlib import Path
import sys
from can.conversions import PDODecoder
from sys import platform

# Play busmaster logs
class LogPlayer():
    def __init__(self):
        self._messagesProcessed = 0

    def messagesProcessed(self):
        return self._messagesProcessed

    def processFile(self, file, reactor, callback, finished, ignoreFailed=True):
        recorded_start_time = None
        last_timestamp = 0
        decoder = PDODecoder()
        file_in = Path(file)
        if platform == 'win32':
            file_in = str(file_in)[1:]

        def cbAndTrack(message):
            self._messagesProcessed += 1
            callback(message)

        with open(file_in, 'r') as input:
            for line in input:
                if line.startswith('***'):
                    continue
                fields = line.split(' ')

                # Do maths to get proper times for replay
                timestring = fields[0]
                # Busmaster timestamp format 16:21:32:6459
                timestamp = datetime.datetime.strptime(timestring, '%H:%M:%S:%f')

                if recorded_start_time is None:
                    recorded_start_time = timestamp
                remaining_gap = timestamp - recorded_start_time

                last_timestamp = timestamp

                id = fields[3][2:]
                data = ''.join(fields[6:-1])
                message = decoder.decode_pdo(int(id, 16), bytes.fromhex(data))

                if message:
                    reactor.callLater(remaining_gap.total_seconds(), cbAndTrack, message)

            finished_gap = last_timestamp - recorded_start_time
            reactor.callLater(finished_gap.total_seconds(), finished, True)