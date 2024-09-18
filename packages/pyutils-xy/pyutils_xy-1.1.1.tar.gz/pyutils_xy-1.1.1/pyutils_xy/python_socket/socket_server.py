# @Coding: UTF-8
# @Time: 2024/9/11 2:41
# @Author: xieyang_ls
# @Filename: socket_server.py

import socket

from logging import info, error, INFO, basicConfig

from pyutils_xy.util import Assemble, HashAssemble

basicConfig(level=INFO)


class SocketServer:
    __sessions = None

    def __init__(self, host: str, port: int, buffer_size: int = 1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socketServer = socket.socket()
        self.socketServer.bind((self.host, self.port))
        self.socketServer.listen(10)
        self.__sessions: Assemble[int, socket] = HashAssemble()
        self.__start_connection()

    def __start_connection(self):
        session, addr = self.socketServer.accept()
        info(f"Connected to {addr}, listening on {self.host}:{self.port} successfully")
        print(hash(addr[1]))
        self.__sessions.put(addr[1], session)
        self.__keep_connection()

    def __keep_connection(self):
        while True:
            port: int = int(input("请输入端口号选择你要聊天的对象: "))
            print(hash(port))
            if port == "exit":
                self.__stop_connection()
                return
            proxy = self.__sessions.get(port)
            if proxy is not None:
                data = proxy.recv(self.buffer_size).decode('utf-8')
                info(f"对方发送一条消息: {data}")
                msg: str = input("请输入你要发送的消息: ")
                proxy.send(msg.encode("utf-8"))
            else:
                error("该端口号不存在，请重新输入")

    def __stop_connection(self):
        info(f"Connection ready to close")
        self.socketServer.close()
        info(f"Connection closed")
