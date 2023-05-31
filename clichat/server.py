"""
Module Docstring
"""
import _thread
import socket
import threading

import snoop
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

print_lock = threading.Lock()


@snoop
def threaded(clt):
    """"""
    while True:
        data = clt.recv(1024)
        if not data:
            print("Bye")
            # lock released on exit.
            print_lock.release()
            break
        data = data[::-1]
        clt.send(data)
    clt.close()


def main():
    host = ""
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket binding to port", port)

    s.listen(5)
    print("socket listening")

    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print("Connected to :", addr[0], ":", addr[1])
        _thread.start_new_thread(threaded, (c,))
    s.close()


if __name__ == "__main__":
    main()
