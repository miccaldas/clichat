"""
Module Docstring
"""
import _thread
import os
import socket
import subprocess

import snoop
from snoop import pp


def type_watch(source, value):
    return f"type({source})", type(value)


snoop.install(watch_extras=[type_watch])


host = ""
port = 2004
ThreadCount = 0

s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s_server.bind((host, port))
except socket.error as e:
    print(str(e))
print("Socket is listening")
s_server.listen(5)
clients = []


@snoop
def broadcast(connection, addr, response):
    for client in clients:
        client.send(response.encode("utf-8"))


@snoop
def multi_client(connection):
    connection.send(str.encode("Server is working."))
    while True:
        data = connection.recv(2048)
        response = f'Server message: {data.decode("utf-8")}'
        if not data:
            print("Not data")
            break
        broadcast(connection, addr, response)
    connection.close()


def recv_available():
    """
    Ascertains if there's anything on the
    TCP receive buffer for a given address.
    """
    adr = f'"{addr[0]}:{str(addr[1])}"'

    ss = subprocess.Popen(
        ["ss", "-a"],
        stdout=subprocess.PIPE,
    )
    grep = subprocess.Popen(
        ["grep", f"{adr}"],
        stdin=ss.stdout,
        stdout=subprocess.PIPE,
    )
    awk = subprocess.Popen(
        ["awk", "{if ($3 > 0) print $3}"],
        stdin=grep.stdout,
        stdout=subprocess.PIPE,
    )
    end_of_pipe = awk.stdout

    return end_of_pipe


while True:
    connection, addr = s_server.accept()
    clients.append(connection)
    print(f"Connected to: {addr[0]}: {str(addr[1])}")
    recbuffer = recv_available()
    print(f"recv buffer is {recbuffer} in size.")
    _thread.start_new_thread(multi_client, (connection,))
    ThreadCount += 1
    print(f"Thread number: {ThreadCount}")
s_server.close()
