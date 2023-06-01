"""
Module Docstring
"""
import snoop
from snoop import pp
import os
import socket
import _thread


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


host = ""
port = 2004
ThreadCount = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))
print("Socket is listening")
s.listen(5)


def multi_client(connection):
    connection.send(str.encode("Server is working."))
    while True:
        data = connection.recv(2048)
        response = f'Server message: {data.decode("utf-8")}'
        if not data:
            print("Not data")
            break
        connection.sendall(str.encode(response))
    connection.close()


while True:
    c, addr = s.accept()
    print(f"Connected to: {addr[0]}: {str(addr[1])}")
    _thread.start_new_thread(multi_client, (c,))
    ThreadCount += 1
    print(f"Thread number: {ThreadCount}")
s.close()


if __name__ == "__main__":
    multi_client()
