#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from threading import Thread, Event
import os
from datetime import datetime
import network
from getch import getch

MSG_LEN = 128
PORT = 11719


class Log(Thread):
    def __init__(self, event):
        super(Log, self).__init__()
        self.log = ''
        self.reader = network.Reader(PORT, MSG_LEN)
        self.event = event

    def run(self):
        while True:
            msg = self.reader.read()
            if msg:
                self.log += "%s\n" % msg.decode("utf-8")
                self.event.set()


class Message(Thread):
    def __init__(self, event):
        super(Message, self).__init__()
        self.msg = ''
        self.event = event

    def run(self):
        while True:
            ch = getch()
            self.msg += ch
            self.event.set()


class Chat():
    def __init__(self):
        self.logger_event = Event()
        self.messenger_event = Event()
        self.logger = Log(self.logger_event)
        self.messenger = Message(self.messenger_event)
        self.writer = network.Writer(PORT)
        self.username = input("Write your username, it's can't be empty: ")
        while self.username == '':
            self.username = input("Write your username, it's can't be empty: ")

    @staticmethod
    def cls():
        os.system(['clear', 'cls'][os.name == os.sys.platform])

    def refresh(self):
        Chat.cls()
        print(self.logger.log)
        print("%s: %s" % (self.username, self.messenger.msg))

    def start(self):
        self.refresh()
        self.logger.start()
        self.messenger.start()
        while True:
            logger_waiting = self.logger_event.wait(0.01)
            if logger_waiting:
                self.refresh()
                self.logger_event.clear()
            messenger_waiting = self.messenger_event.wait(0.01)
            if messenger_waiting:
                if ord(self.messenger.msg[-1]) == 127:
                    self.messenger.msg = self.messenger.msg[:-2]
                    self.refresh()
                    self.messenger_event.clear()
                elif self.messenger.msg[-1] != '\r':
                    self.refresh()
                    self.messenger_event.clear()
                else:
                    msg = self.messenger.msg
                    self.messenger.msg = ''
                    msg = "%s(%s): %s" % (
                        self.username,
                        datetime.strftime(datetime.now(), "%H:%M:%S"),
                        msg
                    )
                    msg = msg.encode("utf-8")
                    self.writer.write(msg)
                self.messenger_event.clear()


if __name__ == "__main__":
    chat = Chat()
    chat.start()