import time
import datetime
from pathlib import Path
import sys
from candata.conversions import PDODecoder
from sys import platform

class LogPlayerJob():
    def __init__(self, file, reactor, callback, finished, ignoreFailed=True):
        self._callIDs = []
        self._file = file
        self._reactor = reactor
        self._callback = callback
        self._finished = finished

    def onMessage(self, message):
        self._callIDs.pop(0)
        self._callback(message)

    def onFinish(self):
        self._finished()

    def start(self):
        recorded_start_time = None
        last_timestamp = 0
        decoder = PDODecoder()
        file_in = Path(self._file)
        if platform == 'win32':
            file_in = str(file_in)[1:]

        with open(file_in, 'r') as input:
            for line in input:
                if line.startswith('***') or line == '\n':
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
                    self._callIDs.append(self._reactor.callLater(remaining_gap.total_seconds(), self.onMessage, message))

            finished_gap = last_timestamp - recorded_start_time
            self._callIDs.append(self._reactor.callLater(finished_gap.total_seconds(), self.onFinish))
    
    def stop(self):
        for callID in self._callIDs:
            callID.cancel()
        self._callIDs.clear()