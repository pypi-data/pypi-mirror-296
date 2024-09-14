# This file is placed in the Public Domain.
# pylint: disable=W0718


"""reactor


SYNOPSIS

    >>> from objr import Reactor
    >>> reactor.register("command", command)
    >>> reactor.start()


INSTALL

    $ pip install objr


DESCRIPTION

    OBJR is a threaded, defer exceptions, keep
    on running. callback engine.


COPYRIGHT

    OBJR is Public Domain.

"""


import io
import queue
import threading
import time
import traceback
import _thread


from objt import later, launch


class Reactor:

    "Reactor"

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        "call callback based on event type."
        func = self.cbs.get(evt.type, None)
        if func:
            evt.thr = launch(func, self, evt)

    def loop(self):
        "proces events until interrupted."
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            except Exception as ex:
                time.sleep(1.0)
                later(ex)

    def poll(self):
        "function to return event."
        return self.queue.get()

    def put(self, evt):
        "put event into the queue."
        self.queue.put_nowait(evt)

    def ready(self):
        "wait until queue is empty."
        while 1:
            if self.queue.qsize() == 0:
                break
            time.sleep(0.1)

    def register(self, typ, cbs):
        "register callback for a type."
        self.cbs[typ] = cbs

    def start(self):
        "start the event loop."
        launch(self.loop)

    def stop(self):
        "stop the event loop."
        self.stopped.set()


class Client(Reactor):

    "Client"

    out = None

    def __init__(self, outer=None):
        Reactor.__init__(self)
        self.out = outer

    def display(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)

    def say(self, _channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        if self.out:
            txt = txt.encode('utf-8', 'replace').decode()
            self.out(txt)


def __dir__():
    return (
        'Client',
        'Reactor'
    )
