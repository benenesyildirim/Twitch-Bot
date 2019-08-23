import datetime
import re
import socket
import sqlite3
import sys
import argparse


class TwitchBot:
    CONNECTION = ('irc.chat.twitch.tv', 6667)
    TIMEDELTA = 10  # wait time between two command.

    def __init__(self, token, user, channel):
        try:
            self.token = token
            self.user = user
            self.channel = channel
            self.send_time = datetime.datetime.now()
            self.server = socket.socket()
            self.server.connect(self.CONNECTION)
            self.server.send(bytes('PASS ' + self.token + '\r\n', 'utf-8'))
            self.server.send(bytes('NICK ' + self.user + '\r\n', 'utf-8'))
            self.server.send(bytes('JOIN ' + self.channel + '\r\n', 'utf-8'))
            print("> {} {}".format(str(datetime.datetime.now()), 'Connection Successful! Enjoy'))
        except socket.gaierror:
            print("Name or service not know! Check your host name.")
            sys.exit()

    @staticmethod
    def check_command(command):
        command = command.split()
        connect_db = sqlite3.connect('bot.db')
        cursor = connect_db.cursor()
        cursor.execute("SELECT * FROM tb_command WHERE command= ?", command)
        data = cursor.fetchall()
        connect_db.close()

        if len(data) != 0:
            return data[0][2]
        else:
            return None

    @staticmethod
    def add_command(*args):
        try:
            connect_db = sqlite3.connect('bot.db')
            cursor = connect_db.cursor()
            cursor.execute("INSERT INTO tb_command(command, response)VALUES (?,?)", args)
            connect_db.commit()
            connect_db.close()
        except sqlite3.OperationalError as e:
            print(e)

    def get_message(self):
        while True:
            raw_message = self.server.recv(1024).decode('utf-8')
            if raw_message == ":tmi.twitch.tv NOTICE * :Login authentication failed\r\n":
                print('> {} {}'.format(str(datetime.datetime.now()), 'Login authentication failed. Check your token.'))
                sys.exit(1)
            if raw_message == "PING :tmi.twitch.tv\r\n":
                print('> {} {} {}'.format(str(datetime.datetime.now()), 'TWITCH', 'PING'))
                self.server.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                print('< {} {} {}'.format(str(datetime.datetime.now()), 'TWITCH', 'PONG'))
            try:
                v_username = re.search("(!.*@)", raw_message).groups()
                viewer_username = v_username[0][1:-1]
                noncleared_command = re.search("(:!.*)", raw_message).groups()
                command = noncleared_command[0][2:-1]
                print('> {} {} {}'.format(str(datetime.datetime.now()), viewer_username, command))
                return viewer_username, command
            except AttributeError:
                pass

    def send_message(self, viewer_username, command_response):
        receive_time = datetime.datetime.now()
        timedelta = receive_time - self.send_time
        if timedelta.seconds > self.TIMEDELTA and command_response is not None:
            self.server.send(bytes(
                '{} {} : @{} {}\r\n'.format('PRIVMSG', self.channel, viewer_username, command_response),
                'utf-8'))
            print('< {} {}'.format(str(datetime.datetime.now()), command_response))
            self.send_time = datetime.datetime.now()
            command_response = None
            return command_response

    def __del__(self):
        pass
