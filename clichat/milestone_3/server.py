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


host = ""
port = 2004
ThreadCount = 0

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_server:
        s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s_server.bind((host, port))
        except socket.error as e:
            print(str(e))
        print("Socket is listening")
        s_server.listen(5)
        clients = []

        connection, addr = s_server.accept()
        print(f"Connected to: {addr[0]}: {str(addr[1])}")
        clients.append(connection)
        _thread.start_new_thread(multi_client, (connection,))
        ThreadCount += 1
        print(f"Thread number: {ThreadCount}")
