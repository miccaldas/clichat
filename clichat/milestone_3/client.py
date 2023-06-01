"""
Module Docstring
"""
import socket

import snoop
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def client():
    """"""
    host = ""
    port = 2004

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("waiting for connection response")

    try:
        s.connect((host, port))
    except socket.error as e:
        print(str(e))

    while True:
        updt = input("Press 1 for new msgs, 2 to write them and 3 to exit. -> ")
        if updt == "1":
            data = s.recv(1024)
            print(data.decode("utf-8"))
        if updt == "2":
            inpt = input("Msg: ")
            s.send(str.encode(inpt))
        if updt == "3":
            s.close()
            raise SystemExit


if __name__ == "__main__":
    client()
