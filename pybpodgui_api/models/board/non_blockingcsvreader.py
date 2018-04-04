from threading import Thread
from queue import Queue, Empty

class NonBlockingCSVReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = stream
        self._q = Queue()
        self._active = True

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''
            try:
                while self._active:
                    line = next(stream)
                    if line:
                        queue.put(line)
                    else:
                        raise UnexpectedEndOfStream
            except StopIteration:
                self._active = False


        self._t = Thread(target=_populateQueue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            row = self._q.get(block = timeout is not None, timeout = timeout)
            return row
        except Empty:
            return None

    def close(self):
        try:
            self._active = False
        except SystemExit:
            pass

class UnexpectedEndOfStream(Exception): pass