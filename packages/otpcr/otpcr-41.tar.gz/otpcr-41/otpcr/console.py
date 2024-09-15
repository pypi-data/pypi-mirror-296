# This file is placed in the Public Domain.
# pylint: disable=C0413,W0611


"prompt"


import os
import readline
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from .errors  import errors
from .thread  import launch
from .object  import Default
from .main    import Broker, Client, Config, Event, command, debug
from .main    import enable, forever, initer, modnames, parse, spl
from .modules import face


Cfg = Config()
Cfg.mod = "cmd,err,mod,srv,thr"


class Console(Client):

    "Console"

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt      = Event()
        evt.txt  = input("> ")
        evt.type = "command"
        parse(evt, evt.txt)
        return evt

    def raw(self, txt):
        "print text."
        print(txt)


def banner():
    "show banner."
    tme = time.ctime(time.time()).replace("  ", " ")
    debug(f"{Cfg.name.upper()} since {tme}")


def wrap(func):
    "reset console."
    old3 = None
    try:
        old3 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        if old3:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old3)


def main():
    "main"
    parse(Cfg, " ".join(sys.argv[1:]))
    if "v" in Cfg.opts:
        enable(print)
        banner()
    if "i" in Cfg.opts:
        Cfg.mod = ",".join(modnames(face))
        for thr in initer(Cfg.mod, face):
            thr.join()
    csl = Console()
    csl.start()
    forever()


def wraps():
    "Wrap main."
    wrap(main)
    errors(print)


if __name__ == "__main__":
    wraps()
