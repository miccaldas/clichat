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
    host = "localhost"
    port = 2004

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("waiting for connection response")

    try:
        s.connect((host, port))
    except socket.error as e:
        print(str(e))

    data = s.recv(1024)

    while True:
        inpt = input("Hey there: ")
        s.send(str.encode(inpt))
        data = s.recv(1024)
        print(data.decode("utf-8"))
    s.close()


if __name__ == "__main__":
    client()
