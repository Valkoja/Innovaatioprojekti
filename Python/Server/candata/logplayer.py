import time
import datetime
from pathlib import Path
import sys
from candata.conversions import PDODecoder
from candata.logplayerjob import LogPlayerJob
from sys import platform

# Play busmaster logs
class LogPlayer():
    def __init__(self, reactor, msgcb, donecb):
        self._job = None
        self._messagesProcessed = 0
        self._reactor = reactor
        self._messageCallback = msgcb
        self._doneCallback = donecb

    def messagesProcessed(self):
        return self._messagesProcessed

    def onMessage(self, message):
        self._messagesProcessed += 1
        self._messageCallback(message)

    def onFinished(self):
        self._doneCallback()

    def processFile(self, file):
        self._job = LogPlayerJob(file, self._reactor, self.onMessage, self.onFinished)
        self._job.start()

    def stop(self):
        self._job.stop()
