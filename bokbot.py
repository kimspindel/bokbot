# -*- coding: utf-8 -*-i
# NB: the IRC protocol limits message lengths to 512 bytes, not just the
# message part but of course the whole command etc.

import sys
import socket
from botresponse import BotResponder

class BokBot:
    __port = 6667
    __nick = "bokbot"
    __ident = "bokbot"
    __realname = "kims bokbot" 

    __readbuffer = ""
    __joinStatus = False
    __names = []
    
    __prefix = "."


    def __init__(self, host, channel):
        self.__host = host

        self.__s=socket.socket()	
        self.__s.connect((self.__host, self.__port))

        nick_string = "NICK %s\r\n" % self.__nick
        user_string = "USER %s %s plopp :%s\r\n" % (self.__ident,
            self.__host, self.__realname)
        self.__s.send(nick_string.encode())
        self.__s.send(user_string.encode())

        self.__r = BotResponder(channel, self.__nick, self.__prefix)
    
    def __send(self, string):
        self.__s.send(string.encode())
        
    def run(self):
        while 1:
            self.__readbuffer += self.__s.recv(1024).decode()
            temp = self.__readbuffer.split("\r\n")
            self.__readbuffer = temp.pop()

            for line in temp:
                print(line)

                words = line.split(" ")       # split line into words
                if words[0] == "PING":
                    response = self.__r.pong(words[1])
                    self.__send(response)
                else:
                    command = words[1]
                    # response is a list filled with commands/responses
                    response = self.__r.respond(command, line)
                    if response:
                        for r in response:
                            self.__send(r)
