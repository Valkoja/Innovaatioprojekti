from candata.logplayerjob import LogPlayerJob


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
