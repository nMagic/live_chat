#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from threading import Thread, Event
import os
from datetime import datetime
import network
from getch import getch

MSG_LEN = 128
PORT = 11719
IS_WINDOWS = (os.name == "nt")
DEFAULT_ENCODE = "cp866" if IS_WINDOWS else "utf-8"


class Log(Thread):
    def __init__(self, event: Event):
        """
        :param event: Event from the calling code.
        """
        super(Log, self).__init__()
        self.log = ''
        self.reader = network.Reader(PORT, MSG_LEN)
        self.event = event

    def run(self):
        """Repeated reading from the listening port."""
        while True:
            msg = self.reader.read()
            if msg:  # Set event if have new message
                self.log += "%s\n" % msg.decode(DEFAULT_ENCODE)
                self.event.set()


class Message(Thread):
    def __init__(self, event: Event):
        """
        :param event: Event from the calling code.
        """
        super(Message, self).__init__()
        self.msg = ''  # Current message.
        self.event = event

    def run(self):
        """Repeated getting char from the listening port."""
        while True:
            ch = getch()
            self.msg += ch.decode(DEFAULT_ENCODE) if IS_WINDOWS else ch
            self.event.set()


class Chat:
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
        """Clear the screen."""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def refresh(self):
        """Refresh chat view."""
        Chat.cls()
        print(self.logger.log)
        print("%s: %s" % (self.username, self.messenger.msg))

    def logger_action(self):
        """Action at log changing"""
        self.refresh()
        self.logger_event.clear()

    def messenger_action(self):
        """Action at message changing"""
        if ord(self.messenger.msg[-1]) == (8 if IS_WINDOWS else 127):  # Delete 2 symbols if user type backspace key.
            self.messenger.msg = self.messenger.msg[:-2]
            self.refresh()
            self.messenger_event.clear()
        elif self.messenger.msg[-1] == '\r':  # Send message if user type enter key.
            msg = self.messenger.msg
            self.messenger.msg = ''
            msg = "%s(%s): %s" % (  # username(HH:MM:SS): msg
                self.username,
                datetime.strftime(datetime.now(), "%H:%M:%S"),
                msg
            )
            msg = msg.encode(DEFAULT_ENCODE)
            self.writer.write(msg)
        else:
            self.refresh()
            self.messenger_event.clear()
        self.messenger_event.clear()

    def start(self):
        """Start method. Check events and do relevant actions."""
        self.refresh()
        self.logger.start()
        self.messenger.start()
        while True:
            logger_waiting = self.logger_event.wait(0.01)
            messenger_waiting = self.messenger_event.wait(0.01)
            if logger_waiting:
                self.logger_action()
            if messenger_waiting:
                self.messenger_action()


if __name__ == "__main__":
    chat = Chat()
    chat.start()
