"""
Module Docstring
"""
import socket

import snoop
from dotenv import load_dotenv
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])

load_dotenv()


@snoop
def client():
    """"""
    host = "localhost"
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    message = "johnny says geeksforgeeks"

    while True:
        s.send(message.encode("ascii"))
        data = s.recv(1024)
        print("Received from the server :", str(data.decode("ascii")))
        ans = input("\nDo you want to continue(y/n) :")
        if ans == "y":
            continue
        else:
            break

    s.close()


if __name__ == "__main__":
    client()
